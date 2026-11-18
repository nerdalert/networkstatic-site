#!/usr/bin/env python3
"""Compare directly fetched public live pages with allowlisted backup content."""
from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from convert import read_table, shortcode_convert, shortcode_media_refs  # noqa: E402
from inventory import normalized_path, source_slug  # noqa: E402
from parse_live_observations import ArticlePage, digest  # noqa: E402


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def page_path(page: dict[str, str], byid: dict[str, dict[str, str]], cache: dict[str, str]) -> str:
    if page["ID"] in cache:
        return cache[page["ID"]]
    parent = byid.get(page.get("post_parent", "0"))
    value = source_slug(page)
    if parent and parent.get("post_type") == "page":
        value = page_path(parent, byid, cache).strip("/") + "/" + value
    cache[page["ID"]] = value
    return value


def canonical_media(value: str) -> str:
    parsed = urlparse(html.unescape(value.strip()))
    path = unquote(parsed.path)
    marker = "/wp-content/uploads/"
    if marker in path:
        path = marker + path.split(marker, 1)[1]
        path = re.sub(r"-\d{2,4}x\d{2,4}(?=\.[^.]+$)", "", path)
        return path
    if parsed.hostname:
        return parsed.hostname.lower().removeprefix("www.") + path
    return path


def media_set(article: ArticlePage, extra: set[str] | None = None) -> set[str]:
    result = set(article.media)
    result.update(article.featured)
    if extra:
        result.update(extra)
    return {canonical_media(value) for value in result if value}


def route_article(html_path: Path) -> ArticlePage:
    parser = ArticlePage()
    parser.feed(html_path.read_text(encoding="utf-8", errors="replace"))
    return parser


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sql", type=Path, required=True)
    ap.add_argument("--sitemap-inventory", type=Path, default=ROOT / "reports/live-sitemap-observations.csv")
    ap.add_argument("--rest-inventory", type=Path, default=ROOT / "reports/live-rest-observations.csv")
    ap.add_argument("--output", type=Path, default=ROOT / "reports/live-content-comparison.csv")
    ap.add_argument("--summary", type=Path, default=ROOT / "reports/live-content-comparison.md")
    args = ap.parse_args()

    sql = args.sql.read_text(encoding="utf-8", errors="replace")
    all_rows = list(read_table(sql, "posts"))
    byid = {row["ID"]: row for row in all_rows}
    eligible = [row for row in all_rows if row.get("post_type") in ("post", "page")
                and row.get("post_status") == "publish" and row.get("post_password", "") == ""]
    metadata = defaultdict(dict)
    for row in read_table(sql, "postmeta"):
        key = row.get("meta_key", "")
        if key and key not in metadata[row["post_id"]]:
            metadata[row["post_id"]][key] = row.get("meta_value", "")
    attachments = {row["ID"]: metadata[row["ID"]].get("_wp_attached_file", "")
                   for row in all_rows if row.get("post_type") == "attachment"}

    live_by_path = {normalized_path(row.get("path") or row.get("url", "")): row
                    for row in read_csv(args.sitemap_inventory)}
    rest_by_path = {normalized_path(row.get("route", "")): row for row in read_csv(args.rest_inventory)}
    rows = []
    for post in sorted(eligible, key=lambda row: (row.get("post_date", ""), int(row["ID"]))):
        route = "/" + (source_slug(post) if post.get("post_type") == "post" else page_path(post, byid, {})) + "/"
        path = normalized_path(route)
        live = live_by_path.get(path, {})
        status = live.get("fetch_http_status", "")
        article_file = ROOT / live.get("fetch_saved_file", "") if live.get("fetch_saved_file") else None
        rest = rest_by_path.get(path, {})
        rest_item = None
        if rest.get("result") == "matched" and rest.get("saved_file"):
            try:
                response = json.loads((ROOT / rest["saved_file"]).read_text(encoding="utf-8"))
                rest_item = next((item for item in response if str(item.get("id", "")) == rest.get("wp_id")), None)
            except (OSError, json.JSONDecodeError, TypeError):
                rest_item = None

        raw = post.get("post_content", "")
        rendered_source, shortcode_issues = shortcode_convert(raw)
        source_parser = ArticlePage()
        source_parser.feed('<div class="entry-content">' + rendered_source + "</div>")
        thumbnail = metadata[post["ID"]].get("_thumbnail_id", "")
        featured = attachments.get(thumbnail, "") if thumbnail else ""
        if featured:
            source_parser.featured.add("/wp-content/uploads/" + featured.lstrip("/"))
        source = source_parser.result()

        if status != "200" or not article_file or not article_file.is_file() or rest_item is None:
            rows.append({"wp_id": post["ID"], "type": post["post_type"], "path": path,
                         "source_status": "publish", "source_password_protected": "no",
                         "live_http_status": status or "not fetched", "live_wp_id": rest.get("wp_id", ""),
                         "live_source_status": rest.get("source_status", "not observed"),
                         "live_password_protected": rest.get("password_protected", "not observed"),
                         "live_content_source": "anonymous WordPress REST API" if rest else "not fetched",
                         "live_title": live.get("title", ""),
                         "source_title": html.unescape(post.get("post_title", "")),
                         "comparison_status": "live-route-not-fetched",
                         "body_text_exact": "n/a", "code_exact": "n/a", "links_exact": "n/a", "media_exact": "n/a",
                         "comparison_notes": "A direct HTTP 200 article/page body is required for content comparison."})
            continue

        current = ArticlePage()
        current.feed('<div class="entry-content">' + (rest_item.get("content", {}).get("rendered", "") or "") + "</div>")
        live_result = current.result()
        direct = route_article(article_file)
        direct_result = direct.result()
        source_media = media_set(source_parser)
        live_media = media_set(current)
        live_media.update(canonical_media(value) for value in json.loads(direct_result["featured_media_paths"]))
        external_refs = shortcode_media_refs(raw)
        source_media.update(canonical_media("/wp-content/uploads/" + value.lstrip("/")) for value in external_refs)

        text_exact = source["body_text_sha256"] == live_result["body_text_sha256"]
        code_exact = source["code_sha256"] == live_result["code_sha256"] and int(source_parser.result()["code_block_count"]) == int(live_result["code_block_count"])
        links_exact = source["links_sha256"] == live_result["links_sha256"]
        media_exact = source_media == live_media
        source_title = unicodedata.normalize("NFC", html.unescape(post.get("post_title", "")).strip())
        live_title = unicodedata.normalize("NFC", html.unescape(rest_item.get("title", {}).get("rendered", "") or live.get("title", "")).strip())
        title_exact = source_title == live_title
        body_exact = text_exact and code_exact and links_exact and media_exact
        comparison_status = "body-exact" if body_exact else "body-differs"
        if not title_exact:
            comparison_status += "; title-differs"

        notes = []
        if not title_exact:
            notes.append("live title differs from the backup title")
        if shortcode_issues:
            notes.append("source shortcode conversion exceptions: " + "|".join(shortcode_issues))
        if source_media != live_media:
            notes.append("source/live media path sets differ after responsive-image size normalization")
        if not text_exact:
            notes.append("normalized visible-text hashes differ")
        if not code_exact:
            notes.append("code sample counts or hashes differ")
        if not links_exact:
            notes.append("visible link text/destination hashes differ")
        if not notes:
            notes.append("normalized visible text, code, links and media paths match")
        if rest_item.get("status") != "publish" or rest_item.get("content", {}).get("protected") is not False:
            notes.append("live REST source is not verified as published and unprotected")
        if (direct_result["body_text_sha256"] != live_result["body_text_sha256"]
                or direct_result["code_sha256"] != live_result["code_sha256"]
                or direct_result["links_sha256"] != live_result["links_sha256"]):
            notes.append("direct page extraction differs from REST rendered body; retain both evidence records")

        rows.append({
            "wp_id": post["ID"], "type": post["post_type"], "path": path,
            "source_status": "publish", "source_password_protected": "no",
            "live_http_status": status, "sitemap_type": live.get("sitemap_type", ""),
            "live_wp_id": rest_item.get("id", ""), "live_source_status": rest_item.get("status", ""),
            "live_password_protected": str(bool(rest_item.get("content", {}).get("protected", True))).lower(),
            "live_content_source": "anonymous WordPress REST API; matched exact route",
            "live_content_sha256": rest.get("content_sha256", ""),
            "source_title": source_title, "live_title": live_title,
            "title_exact": "yes" if title_exact else "no",
            "source_published": post.get("post_date_gmt", ""), "live_published": live.get("published", ""),
            "source_modified": post.get("post_modified_gmt", ""), "live_lastmod": rest_item.get("modified_gmt", live.get("lastmod", "")),
            "source_text_chars": source["body_text_chars"], "live_text_chars": live_result["body_text_chars"],
            "body_text_exact": "yes" if text_exact else "no",
            "source_text_sha256": source["body_text_sha256"], "live_text_sha256": live_result["body_text_sha256"],
            "source_code_count": source["code_block_count"], "live_code_count": live_result["code_block_count"],
            "code_exact": "yes" if code_exact else "no",
            "source_code_sha256": source["code_sha256"], "live_code_sha256": live_result["code_sha256"],
            "source_link_count": source["link_count"], "live_link_count": live_result["link_count"],
            "links_exact": "yes" if links_exact else "no",
            "source_links_sha256": source["links_sha256"], "live_links_sha256": live_result["links_sha256"],
            "source_media_count": len(source_media), "live_media_count": len(live_media),
            "media_exact": "yes" if media_exact else "no",
            "source_media_paths": json.dumps(sorted(source_media), ensure_ascii=False),
            "live_media_paths": json.dumps(sorted(live_media), ensure_ascii=False),
            "live_rest_vs_page_text_exact": "yes" if direct_result["body_text_sha256"] == live_result["body_text_sha256"] else "no",
            "live_rest_vs_page_code_exact": "yes" if direct_result["code_sha256"] == live_result["code_sha256"] else "no",
            "live_rest_vs_page_links_exact": "yes" if direct_result["links_sha256"] == live_result["links_sha256"] else "no",
            "comparison_status": comparison_status, "comparison_notes": "; ".join(notes),
        })

    fields = ["wp_id", "type", "path", "source_status", "source_password_protected", "live_http_status", "sitemap_type",
              "live_wp_id", "live_source_status", "live_password_protected", "live_content_source", "live_content_sha256",
              "source_title", "live_title", "title_exact", "source_published", "live_published", "source_modified", "live_lastmod",
              "source_text_chars", "live_text_chars", "body_text_exact", "source_text_sha256", "live_text_sha256",
              "source_code_count", "live_code_count", "code_exact", "source_code_sha256", "live_code_sha256",
              "source_link_count", "live_link_count", "links_exact", "source_links_sha256", "live_links_sha256",
              "source_media_count", "live_media_count", "media_exact", "source_media_paths", "live_media_paths",
              "live_rest_vs_page_text_exact", "live_rest_vs_page_code_exact", "live_rest_vs_page_links_exact",
              "comparison_status", "comparison_notes"]
    write_csv(args.output, rows, fields)
    exact_counts = {key: sum(row.get(key) == "yes" for row in rows)
                    for key in ("title_exact", "body_text_exact", "code_exact", "links_exact", "media_exact")}
    full_body = sum(row.get("comparison_status", "").startswith("body-exact") for row in rows)
    api_public = sum(row.get("live_source_status") == "publish" for row in rows)
    api_unprotected = sum(row.get("live_password_protected") == "false" for row in rows)
    rest_page_counts = {key: sum(row.get(key) == "yes" for row in rows)
                        for key in ("live_rest_vs_page_text_exact", "live_rest_vs_page_code_exact", "live_rest_vs_page_links_exact")}
    notes = ["# Live content comparison", "",
             f"Compared {len(rows)} public, unprotected backup post/page sources with directly fetched live routes and their anonymous WordPress REST bodies.",
             f"Text, code, link, media and title exact counts: `{exact_counts}`.",
             f"Full body matches (text/code/links/media): {full_body}/{len(rows)}.",
             f"Live REST status and password checks passed for {api_public}/{len(rows)} (`status=publish`) and {api_unprotected}/{len(rows)} (`content.protected=false`). Direct-page versus REST normalized text/code/link matches are `{rest_page_counts}`.",
             "REST rows also record live post ID, exact route match, body hash, and modified date. A live-versus-backup mismatch is not automatically a conversion loss; `conversion-fidelity.csv` separately compares every converted review page with its backup source. Six per-article local link exceptions and three external-media exceptions remain documented.",
             "The April 17 live-only post is not included here because it is absent from the supplied backup; its verification is tracked in `content-verification.csv` and `live-source-eligibility.csv`."]
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text("\n".join(notes) + "\n", encoding="utf-8")
    print(f"Live content comparison: {full_body}/{len(rows)} full body matches; exact={exact_counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
