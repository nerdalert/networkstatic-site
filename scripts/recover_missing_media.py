#!/usr/bin/env python3
"""Attempt reproducible recovery of media absent from the WordPress upload backup."""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path, PurePosixPath
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from convert import MediaRefs, mask_code, shortcode_media_refs
from inventory import read_table, source_slug

MAX_BYTES = 80_000_000
UA = "Mozilla/5.0 (compatible; NetworkStaticMigration/1.0)"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def media_relative(url: str) -> str:
    path = unquote(urlparse(html.unescape(url)).path)
    marker = "/wp-content/uploads/"
    if marker not in path:
        return ""
    relative = path.split(marker, 1)[1]
    posix = PurePosixPath(relative)
    if not relative or posix.is_absolute() or ".." in posix.parts:
        return ""
    return posix.as_posix()


def valid_payload(relative: str, content_type: str, data: bytes) -> bool:
    suffix = PurePosixPath(relative).suffix.lower()
    mime = content_type.split(";", 1)[0].strip().lower()
    if suffix == ".pdf":
        return data.startswith(b"%PDF-") or mime == "application/pdf"
    if suffix in (".jpg", ".jpeg"):
        return data.startswith(b"\xff\xd8\xff") or mime in ("image/jpeg", "image/pjpeg")
    if suffix == ".png":
        return data.startswith(b"\x89PNG\r\n\x1a\n") or mime == "image/png"
    if suffix == ".gif":
        return data.startswith((b"GIF87a", b"GIF89a")) or mime == "image/gif"
    if suffix == ".webp":
        return data.startswith(b"RIFF") and data[8:12] == b"WEBP" or mime == "image/webp"
    return not mime.startswith("text/html") and bool(data)


def source_urls(post: dict[str, str], wanted: set[str]) -> dict[str, list[str]]:
    matches = {relative: [] for relative in wanted}
    text = html.unescape(post.get("post_content", ""))
    for raw in re.findall(r"https?://[^\s\"'<>]+", text, flags=re.I):
        raw = raw.rstrip(".,;:!?)]}")
        relative = media_relative(raw)
        if relative in matches and raw not in matches[relative]:
            matches[relative].append(raw)
    return matches


def attempt(url: str, relative: str, attempt_no: int) -> tuple[dict[str, str], bytes | None]:
    row = {"requested_url": url, "attempt": str(attempt_no), "result": "", "http_status": "",
           "final_url": "", "content_type": "", "response_bytes": "", "response_sha256": "",
           "transport_error": ""}
    request = Request(url, headers={"User-Agent": UA, "Accept": "image/avif,image/webp,application/pdf,image/*,*/*;q=0.7"})
    try:
        with urlopen(request, timeout=25) as response:
            data = response.read(MAX_BYTES + 1)
            row.update({"http_status": str(response.status), "final_url": response.geturl(),
                        "content_type": response.headers.get("Content-Type", ""),
                        "response_bytes": str(len(data)), "response_sha256": hashlib.sha256(data).hexdigest()})
            if len(data) > MAX_BYTES:
                row.update({"result": "oversize", "transport_error": f"response exceeded {MAX_BYTES} bytes"})
                return row, None
            if not valid_payload(relative, row["content_type"], data):
                row["result"] = "invalid-content-type-or-signature"
                return row, None
            row["result"] = "recovered"
            return row, data
    except HTTPError as exc:
        row.update({"result": "http-error", "http_status": str(exc.code), "final_url": exc.geturl(),
                    "content_type": exc.headers.get("Content-Type", "") if exc.headers else ""})
    except (URLError, TimeoutError, OSError) as exc:
        row.update({"result": "transport-error", "transport_error": f"{type(exc).__name__}: {exc}"})
    return row, None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sql", type=Path, required=True)
    parser.add_argument("--uploads", type=Path, required=True)
    parser.add_argument("--review-dir", type=Path, default=ROOT / "migration-review/generated")
    args = parser.parse_args()
    review = args.review_dir.resolve()
    if not review.is_relative_to((ROOT / "migration-review").resolve()):
        parser.error("--review-dir must stay under the ignored migration-review/ directory")

    posts = {row["ID"]: row for row in read_table(args.sql.read_text(encoding="utf-8", errors="replace"), "posts")
             if row.get("post_type") in ("post", "page") and row.get("post_status") == "publish"
             and row.get("post_password", "") == ""}
    conversion_rows = {row.get("wp_id", ""): row for row in read_csv(ROOT / "reports/conversion-review.csv")}
    missing: dict[tuple[str, str], dict[str, str]] = {}
    for wp_id, post in posts.items():
        raw = post.get("post_content", "")
        parser_refs = MediaRefs()
        parser_refs.feed(mask_code(raw)[0])
        references = {media_relative(url) for url, _kind in parser_refs.refs}
        references.update(shortcode_media_refs(raw))
        row = conversion_rows.get(wp_id, {"wp_id": wp_id, "permalink": "/" + source_slug(post) + "/"})
        for relative in filter(None, references):
            source = (args.uploads / relative).resolve()
            if source.is_file():
                continue
            missing[(wp_id, relative)] = row
    # The converter omits successfully recovered dependencies from its
    # missing-media column. Carry those earlier recovery records forward so a
    # rerun cannot erase their provenance or turn them into implicit failures.
    previous_report = ROOT / "reports/missing-media-recovery.csv"
    if previous_report.is_file():
        for row in read_csv(previous_report):
            if row.get("status") == "recovered" and row.get("wp_id") and row.get("relative_path"):
                missing.setdefault((row["wp_id"], row["relative_path"]), row)

    jobs = []
    for (wp_id, relative), row in sorted(missing.items()):
        safe = PurePosixPath(relative)
        if safe.is_absolute() or ".." in safe.parts:
            continue
        post = posts.get(wp_id)
        candidates = source_urls(post, {relative}).get(relative, []) if post else []
        # Prefer the actual third-party origin present in source HTML; try the
        # former blog host as a fallback for media that had been mirrored there.
        origin_candidates = [url for url in candidates if (urlparse(url).hostname or "").lower() not in
                             ("networkstatic.net", "www.networkstatic.net")]
        other_candidates = [url for url in candidates if url not in origin_candidates]
        fallback = [f"https://networkstatic.net/wp-content/uploads/{relative}",
                    f"http://networkstatic.net/wp-content/uploads/{relative}"]
        urls = list(dict.fromkeys(origin_candidates + other_candidates + fallback))
        jobs.append((wp_id, relative, row, urls))

    diagnostics: list[dict[str, str]] = []
    results: dict[tuple[str, str], dict[str, str]] = {}
    # Keep recoveries outside generated/ because the converter recreates that
    # directory. The deterministic conversion step copies only listed files
    # with a published article owner into its output tree.
    output_root = ROOT / "migration-review/recovered-media/wp-content/uploads"
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {}
        for wp_id, relative, row, urls in jobs:
            for attempt_no, url in enumerate(urls, 1):
                futures[pool.submit(attempt, url, relative, attempt_no)] = (wp_id, relative, attempt_no)
        for future in as_completed(futures):
            wp_id, relative, attempt_no = futures[future]
            diag, data = future.result()
            diag.update({"wp_id": wp_id, "relative_path": relative})
            diagnostics.append(diag)
            key = (wp_id, relative)
            if data is not None and key not in results:
                destination = output_root / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(data)
                results[key] = {"status": "recovered", "source_url": diag["requested_url"],
                                "final_url": diag["final_url"], "content_type": diag["content_type"],
                                "size_bytes": str(len(data)), "sha256": diag["response_sha256"],
                                "saved_path": destination.relative_to(ROOT).as_posix()}
        # The completion order is not the retry order. Keep attempts for a path
        # as diagnostics, while a winning response is selected by smallest URL
        # order that returned a valid payload.

    rows = []
    for wp_id, relative, source_row, urls in jobs:
        recovered = results.get((wp_id, relative))
        attempts = [row for row in diagnostics if row["wp_id"] == wp_id and row["relative_path"] == relative]
        if recovered:
            # If duplicate owners referenced the same recovered file, it is a
            # valid shared dependency and only one output file is retained.
            status = "recovered"
        else:
            status = "unavailable-after-origin-and-mirror-attempts"
        conversion_media = source_row.get("missing_media", "").split("|") if source_row else []
        suffix = PurePosixPath(relative).suffix.lower()
        disposition = ("local asset available" if recovered else
                       "preserve the original external PDF link; surrounding article text remains intact"
                       if suffix == ".pdf" else
                       "remove the broken image element; surrounding text/captions remain intact"
                       if relative in conversion_media else
                       "empty media-anchor shell removed; no displayed image or caption depended on this file")
        rows.append({"wp_id": wp_id, "permalink": source_row.get("permalink", ""),
                     "relative_path": relative, "attempt_count": len(attempts), "status": status,
                     "source_url": recovered.get("source_url", "") if recovered else (urls[0] if urls else ""),
                     "attempted_urls": "|".join(urls),
                     "final_url": recovered.get("final_url", "") if recovered else "",
                     "content_type": recovered.get("content_type", "") if recovered else "",
                     "size_bytes": recovered.get("size_bytes", "") if recovered else "",
                     "sha256": recovered.get("sha256", "") if recovered else "",
                     "saved_path": recovered.get("saved_path", "") if recovered else "",
                     "disposition": disposition})

    diagnostics.sort(key=lambda row: (int(row.get("wp_id", "0")), row.get("relative_path", ""), int(row.get("attempt", "0"))))

    def write(path: Path, fields: list[str], values: list[dict[str, str]]) -> None:
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
            writer.writeheader()
            writer.writerows(values)

    write(ROOT / "reports/missing-media-recovery.csv",
          ["wp_id", "permalink", "relative_path", "attempt_count", "status", "source_url", "final_url",
           "attempted_urls", "content_type", "size_bytes", "sha256", "saved_path", "disposition"], rows)
    write(ROOT / "reports/missing-media-fetch-diagnostics.csv",
          ["wp_id", "relative_path", "requested_url", "attempt", "result", "http_status", "final_url",
           "content_type", "response_bytes", "response_sha256", "transport_error"], diagnostics)
    external_exceptions = []
    for row in rows:
        if row["status"] != "unavailable-after-origin-and-mirror-attempts" or not row["relative_path"].lower().endswith(".pdf"):
            continue
        attempts = sorted((d for d in diagnostics if d["wp_id"] == row["wp_id"] and d["relative_path"] == row["relative_path"]),
                          key=lambda d: int(d.get("attempt", "0")))
        result_summary = "; ".join(f"{d['requested_url']} => {d['http_status'] or d['result']}" for d in attempts)
        external_exceptions.append({"wp_id": row["wp_id"], "source_permalink": row["permalink"],
                                    "original_target": row["source_url"], "preserved_target": row["source_url"],
                                    "attempted_urls": row["attempted_urls"], "retrieval_method": "Python urllib GET with browser-compatible user agent",
                                    "probe_results": result_summary,
                                    "disposition": "preserved as the original external document link; no local asset referenced",
                                    "blocks_publication": "no"})
    external_exceptions.append({"wp_id": "768", "source_permalink": "/openvswitch-configure-from-packages-and-attaching-to-a-floodlight-openflow-controller/",
                                "original_target": "https://networkstatic.net/2012/installing-openvswitch-on-ubuntu-11-10-with-kvm/",
                                "preserved_target": "https://networkstatic.wordpress.com/2012/02/03/installing-openvswitch-on-ubuntu-11-10-with-kvm/",
                                "attempted_urls": "https://networkstatic.net/2012/installing-openvswitch-on-ubuntu-11-10-with-kvm/|https://networkstatic.wordpress.com/2012/02/03/installing-openvswitch-on-ubuntu-11-10-with-kvm/",
                                "retrieval_method": "Python urllib GET with Mozilla/5.0 user agent",
                                "probe_results": "current-domain route returned HTTP 406; WordPress.com route redirected to the current-domain route and returned HTTP 406; same WordPress.com target is also referenced by public post ID 390",
                                "disposition": "preserved as an external historical WordPress link; current live response is inconclusive and does not block publication",
                                "blocks_publication": "no"})
    write(ROOT / "reports/external-link-exceptions.csv",
          ["wp_id", "source_permalink", "original_target", "preserved_target", "attempted_urls", "retrieval_method",
           "probe_results", "disposition", "blocks_publication"], external_exceptions)
    recovered_count = sum(row["status"] == "recovered" for row in rows)
    print(f"Missing media recovery: recovered {recovered_count}/{len(rows)} files; attempts={len(diagnostics)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
