#!/usr/bin/env python3
"""Materialize only ledger-approved WordPress sources into Hugo production roots."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import tomllib
from collections import defaultdict
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8", errors="strict")
    if not text.startswith("+++\n") or "\n+++\n" not in text[4:]:
        raise ValueError(f"invalid TOML front matter: {path.relative_to(ROOT)}")
    end = text.find("\n+++\n", 4)
    return tomllib.loads(text[4:end]), text


def safe_relative(value: str) -> Path:
    path = PurePosixPath(value)
    if not value or path.is_absolute() or ".." in path.parts or "\\" in value:
        raise ValueError(f"unsafe relative path in migration manifest: {value!r}")
    return Path(*path.parts)


def production_frontmatter(text: str) -> str:
    end = text.find("\n+++\n", 4)
    if not text.startswith("+++\n") or end < 0:
        raise ValueError("invalid review front matter while preparing production content")
    header = text[4:end]
    header = re.sub(r"(?m)^review_only = true$", "review_only = false", header)
    header = re.sub(r"(?m)^draft = true$", "draft = false", header)
    if "migration_generated = true" not in header:
        header = header.replace("source_password_protected = false", "source_password_protected = false\nmigration_generated = true", 1)
    return "+++\n" + header + text[end:]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review-dir", type=Path, default=ROOT / "migration-review/generated")
    parser.add_argument("--content-dir", type=Path, default=ROOT / "content")
    parser.add_argument("--static-dir", type=Path, default=ROOT / "static")
    args = parser.parse_args()
    review = args.review_dir.resolve()
    content = args.content_dir.resolve()
    static = args.static_dir.resolve()
    if not review.is_relative_to((ROOT / "migration-review").resolve()):
        parser.error("--review-dir must remain under migration-review/")
    if content != (ROOT / "content").resolve() or static != (ROOT / "static").resolve():
        parser.error("production materialization is fixed to the repository content/ and static/ roots")

    ledger = read_csv(ROOT / "reports/publication-eligibility.csv")
    eligible_rows = [row for row in ledger if row.get("publish_eligible") == "yes"]
    if not eligible_rows:
        raise SystemExit("refusing to materialize an empty publication allowlist")
    approved = {}
    for row in eligible_rows:
        wp_id = row.get("wp_id", "")
        if (not wp_id or row.get("source_status") != "publish"
                or row.get("source_password_protected") != "no"):
            raise SystemExit("publication allowlist contains a source without published/unprotected evidence")
        if wp_id in approved:
            raise SystemExit(f"duplicate approved WordPress ID: {wp_id}")
        if row.get("fidelity_status") not in ("pass", "pass-with-media-exceptions", "pass-live-verified"):
            raise SystemExit(f"approved WordPress ID {wp_id} has no passing automated conversion status")
        approved[wp_id] = row

    audit = json.loads((ROOT / "reports/migration-source-audit.json").read_text(encoding="utf-8"))
    if not audit.get("audit_passed") or not audit.get("assertion_no_nonpublic_or_protected_source_migrated"):
        raise SystemExit("published-source audit did not prove public/unprotected provenance")
    sources = {str(row.get("wp_id")): row for row in audit.get("migrated_sources", [])}

    source_files = {}
    for path in sorted((review / "content").rglob("*.md")):
        front, _ = parse_frontmatter(path)
        wp_id = str(front.get("wp_id", ""))
        if wp_id:
            if wp_id in source_files:
                raise SystemExit(f"duplicate review output for WordPress ID {wp_id}")
            source_files[wp_id] = (path, front)

    content_plan = []
    for wp_id, row in approved.items():
        source = sources.get(wp_id)
        found = source_files.get(wp_id)
        if not source or not found:
            raise SystemExit(f"approved WordPress ID {wp_id} lacks verified source/output evidence")
        path, front = found
        if (source.get("post_status") != "publish" or source.get("password_protected") is not False
                or front.get("source_status") != "publish" or front.get("source_password_protected") is not False
                or front.get("draft") is not True or front.get("review_only") is not True
                or front.get("source_content_sha256") != source.get("source_content_sha256")):
            raise SystemExit(f"approved WordPress ID {wp_id} failed its source provenance or review-state audit")
        if front.get("url", "").rstrip("/") != row.get("permalink", "").rstrip("/"):
            raise SystemExit(f"approved WordPress ID {wp_id} route differs between ledger and converted file")
        destination = (content / path.relative_to(review / "content")).resolve()
        if not destination.is_relative_to(content):
            raise SystemExit(f"content destination escaped the production content root: {destination}")
        content_plan.append((wp_id, row, path, destination, source))

    # Remove only content created by this materializer, leaving utility pages and
    # unrelated author-maintained Markdown intact.
    for path in content.rglob("*.md"):
        try:
            front, _text = parse_frontmatter(path)
        except (OSError, ValueError, tomllib.TOMLDecodeError):
            continue
        if front.get("migration_generated") is True:
            path.unlink()

    media_by_path: dict[str, dict] = {}
    eligible_routes = {row.get("permalink", "") for row in eligible_rows}
    for row in read_csv(ROOT / "reports/media-copy-manifest.csv"):
        owners = set(filter(None, row.get("owner_urls", "").split("|")))
        if not owners.intersection(eligible_routes):
            continue
        relative = safe_relative(row.get("source_path", ""))
        key = relative.as_posix()
        current = media_by_path.get(key)
        owners_for_path = set(filter(None, current.get("owner_urls", "").split("|"))) if current else set()
        owners_for_path.update(owners)
        item = dict(row)
        item["owner_urls"] = "|".join(sorted(owners_for_path))
        media_by_path[key] = item
    for row in read_csv(ROOT / "reports/live-recovered-media.csv"):
        route = "/chatgpt-project-docs/"
        if route not in eligible_routes:
            continue
        relative = safe_relative(row.get("source_path", ""))
        key = relative.as_posix()
        current = media_by_path.get(key)
        if current and current.get("sha256") != row.get("sha256"):
            raise SystemExit(f"conflicting media hashes for public dependency {key}")
        owners = set(filter(None, current.get("owner_urls", "").split("|"))) if current else set()
        owners.add(route)
        media_by_path[key] = {"source_path": key, "sha256": row.get("sha256", ""),
                              "size_bytes": row.get("size_bytes", ""), "owner_urls": "|".join(sorted(owners)),
                              "source_origin": "verified live-only public media", "source_url": row.get("source_url", "")}

    media_source_root = review / "static/wp-content/uploads"
    media_plan = []
    for key, row in sorted(media_by_path.items()):
        relative = safe_relative(key)
        source = (media_source_root / relative).resolve()
        destination = (static / "wp-content/uploads" / relative).resolve()
        if not source.is_relative_to(media_source_root.resolve()) or not source.is_file():
            raise SystemExit(f"published media dependency is missing from reviewed source: {key}")
        actual_hash = sha256(source)
        if actual_hash != row.get("sha256"):
            raise SystemExit(f"published media hash differs from its verified report: {key}")
        if not destination.is_relative_to((static / "wp-content/uploads").resolve()):
            raise SystemExit(f"media destination escaped production static root: {destination}")
        media_plan.append((key, row, source, destination, actual_hash))

    # Remove stale migration media using only paths recorded by the prior
    # migration manifest; never sweep arbitrary static assets.
    prior_manifest = ROOT / "reports/published-media-manifest.csv"
    current_media = {item[0] for item in media_plan}
    if prior_manifest.is_file():
        for row in read_csv(prior_manifest):
            key = row.get("relative_path", "")
            if key and key not in current_media:
                old = (static / "wp-content/uploads" / safe_relative(key)).resolve()
                if old.is_relative_to((static / "wp-content/uploads").resolve()) and old.is_file():
                    old.unlink()

    content_manifest = []
    for wp_id, row, source_path, destination, source in content_plan:
        text = source_path.read_text(encoding="utf-8", errors="strict")
        text = production_frontmatter(text)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding="utf-8")
        content_manifest.append({"wp_id": wp_id, "permalink": row.get("permalink", ""),
                                 "type": source.get("post_type", ""), "source_origin": source.get("source_origin", "backup SQL"),
                                 "source_status": source.get("post_status", ""), "password_protected": "no",
                                 "source_content_sha256": source.get("source_content_sha256", ""),
                                 "production_content_path": destination.relative_to(ROOT).as_posix(),
                                 "fidelity_status": row.get("fidelity_status", "")})
    for _key, _row, source, destination, _digest in media_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    write_csv(ROOT / "reports/published-content-manifest.csv",
              ["wp_id", "permalink", "type", "source_origin", "source_status", "password_protected",
               "source_content_sha256", "production_content_path", "fidelity_status"], content_manifest)
    write_csv(ROOT / "reports/published-media-manifest.csv",
              ["relative_path", "sha256", "size_bytes", "owner_urls", "source_origin", "source_url"],
              [{"relative_path": key, "sha256": digest, "size_bytes": row.get("size_bytes", ""),
                "owner_urls": row.get("owner_urls", ""), "source_origin": row.get("source_origin", ""),
                "source_url": row.get("source_url", "")}
               for key, row, _source, _destination, digest in media_plan])
    print(f"Prepared production content: {len(content_plan)} public/unprotected pages; copied {len(media_plan)} owned media files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
