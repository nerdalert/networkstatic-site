#!/usr/bin/env python3
"""Prove that local migration review output contains only public WP sources."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
import tomllib
from collections import Counter, defaultdict
from pathlib import Path

from convert import MediaRefs, mask_code, read_table, remove_empty_anchor_links, rewrite_internal_urls, shortcode_media_refs, shortcode_convert

ROOT = Path(__file__).resolve().parents[1]


def references(post: dict[str, str], thumbnail: str, attachments: dict[str, str]) -> set[str]:
    raw = remove_empty_anchor_links(post.get("post_content", ""))
    parser = MediaRefs()
    parser.feed(mask_code(raw)[0])
    refs: set[str] = set()
    refs.update(shortcode_media_refs(raw))
    for url, _kind in parser.refs:
        from urllib.parse import unquote, urlparse
        path = unquote(urlparse(url).path)
        marker = "/wp-content/uploads/"
        if marker in path:
            refs.add(path.split(marker, 1)[1])
    converted, _shortcodes = shortcode_convert(raw)
    rendered_parser = MediaRefs()
    rendered_parser.feed(mask_code(converted)[0])
    for url, _kind in rendered_parser.refs:
        from urllib.parse import unquote, urlparse
        path = unquote(urlparse(url).path)
        marker = "/wp-content/uploads/"
        if marker in path:
            refs.add(path.split(marker, 1)[1])
    _converted, rewritten, _routes = rewrite_internal_urls(converted)
    refs.update(rewritten)
    if thumbnail and thumbnail in attachments and attachments[thumbnail]:
        refs.add(attachments[thumbnail])
    return refs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sql", type=Path, required=True)
    ap.add_argument("--review-dir", type=Path, default=ROOT / "migration-review/generated")
    ap.add_argument("--uploads", type=Path, required=True)
    ap.add_argument("--report", type=Path, default=ROOT / "reports/migration-source-audit.json")
    args = ap.parse_args()
    review = args.review_dir.resolve()
    if not review.is_relative_to((ROOT / "migration-review").resolve()):
        ap.error("--review-dir must be inside migration-review/")
    sql = args.sql.read_text(encoding="utf-8", errors="replace")
    posts = list(read_table(sql, "posts"))
    byid = {row["ID"]: row for row in posts}
    content = [row for row in posts if row.get("post_type") in ("post", "page")]
    eligible = {row["ID"]: row for row in content
                if row.get("post_status") == "publish" and row.get("post_password", "") == ""}
    excluded_nonpublished = Counter((row.get("post_type", ""), row.get("post_status", ""))
                                    for row in content if row.get("post_status") != "publish")
    protected = [row for row in content if row.get("post_status") == "publish" and row.get("post_password", "") != ""]
    live_sources = {row.get("wp_id", ""): row for row in csv.DictReader(
        (ROOT / "reports/live-source-eligibility.csv").open(encoding="utf-8", newline=""))} if (ROOT / "reports/live-source-eligibility.csv").is_file() else {}
    live_media = list(csv.DictReader((ROOT / "reports/live-recovered-media.csv").open(encoding="utf-8", newline=""))) if (ROOT / "reports/live-recovered-media.csv").is_file() else []
    recovered_media = list(csv.DictReader((ROOT / "reports/missing-media-recovery.csv").open(encoding="utf-8", newline=""))) if (ROOT / "reports/missing-media-recovery.csv").is_file() else []
    metadata = defaultdict(dict)
    for row in read_table(sql, "postmeta"):
        key = row.get("meta_key", "")
        if key and key not in metadata[row["post_id"]]:
            metadata[row["post_id"]][key] = row.get("meta_value", "")
    attachments = {row["ID"]: metadata[row["ID"]].get("_wp_attached_file", "")
                   for row in posts if row.get("post_type") == "attachment"}

    errors: list[str] = []
    records = []
    seen: set[str] = set()
    content_root = review / "content"
    if not content_root.is_dir():
        errors.append("review content directory is missing")
    else:
        for path in sorted(content_root.rglob("*.md")):
            text = path.read_text(encoding="utf-8", errors="replace")
            if not text.startswith("+++\n") or "\n+++\n" not in text[4:]:
                errors.append(f"invalid Hugo front matter: {path.relative_to(ROOT)}")
                continue
            closing = text.find("\n+++\n", 4)
            try:
                fm = tomllib.loads(text[4:closing])
            except tomllib.TOMLDecodeError:
                errors.append(f"unreadable Hugo front matter: {path.relative_to(ROOT)}")
                continue
            wp_id = str(fm.get("wp_id", ""))
            if wp_id in seen:
                errors.append("duplicate WordPress source ID in review content")
            seen.add(wp_id)
            source = byid.get(wp_id)
            if source:
                source_hash = hashlib.sha256(source.get("post_content", "").encode("utf-8")).hexdigest()
                checks = {
                    "content_type_allowed": source.get("post_type") in ("post", "page"),
                    "source_status_is_publish": source.get("post_status") == "publish" and fm.get("source_status") == "publish",
                    "source_password_empty": source.get("post_password", "") == "" and fm.get("source_password_protected") is False,
                    "source_hash_matches": source_hash == fm.get("source_content_sha256"),
                    "hugo_draft_flag_set": fm.get("draft") is True and fm.get("review_only") is True,
                }
                source_type = source.get("post_type", "")
                source_status = source.get("post_status", "")
                password_protected = bool(source.get("post_password", ""))
                if source_status != "publish" or password_protected:
                    errors.append("nonpublic or password-protected WordPress source was found in review content")
            else:
                live = live_sources.get(wp_id)
                if not live:
                    errors.append("review content references a source ID absent from SQL and the verified live-source ledger")
                    continue
                source_hash = live.get("source_content_sha256", "")
                checks = {
                    "content_type_allowed": live.get("source_type") == "live-only REST API",
                    "source_status_is_publish": live.get("source_status") == "publish" and fm.get("source_status") == "publish",
                    "source_password_empty": live.get("password_protected") == "no" and fm.get("source_password_protected") is False,
                    "source_hash_matches": bool(source_hash) and source_hash == fm.get("source_content_sha256"),
                    "hugo_draft_flag_set": fm.get("draft") is True and fm.get("review_only") is True,
                    "live_api_identity_matches": fm.get("live_source_id") == int(wp_id) and fm.get("live_source_status") == "publish",
                    "live_public_route_verified": live.get("route_http_status") == "200" and live.get("anonymous_full_body") == "yes",
                    "live_password_protection_absent": fm.get("live_source_password_protected") is False,
                }
                source_type = "post"
                source_status = live.get("source_status", "")
                password_protected = live.get("password_protected") != "no"
                if source_status != "publish" or password_protected:
                    errors.append("nonpublic or password-protected live-only source was found in review content")
            for check, passed in checks.items():
                if not passed:
                    errors.append(f"{check} failed for migrated source ID {wp_id}")
            records.append({"wp_id": int(wp_id), "post_type": source_type,
                            "source_origin": "backup SQL" if source else "verified live-only REST API",
                            "post_status": source_status, "password_protected": password_protected,
                            "source_content_sha256": source_hash, "review_content_path": path.relative_to(ROOT).as_posix(),
                            "checks": checks})

    expected = set(eligible) | set(live_sources)
    if seen != expected:
        errors.append(f"review source set mismatch: expected {len(expected)} eligible rows, found {len(seen)} review files")
    if seen & (set(byid) - expected):
        errors.append("review output includes a non-allowlisted WordPress source")

    eligible_media: set[str] = set()
    excluded_media: set[str] = set()
    for row in content:
        refs = references(row, metadata[row["ID"]].get("_thumbnail_id", ""), attachments)
        if row["ID"] in eligible:
            eligible_media.update(refs)
        else:
            excluded_media.update(refs)
    for row in live_media:
        eligible_media.add(row.get("source_path", ""))
        output_path = review / "static/wp-content/uploads" / row.get("source_path", "")
        if not output_path.is_file():
            errors.append("verified live-only media is absent from the local review output")
        elif hashlib.sha256(output_path.read_bytes()).hexdigest() != row.get("sha256"):
            errors.append("verified live-only media hash changed in the local review output")
    for row in recovered_media:
        if row.get("status") != "recovered":
            continue
        relative = row.get("relative_path", "")
        eligible_media.add(relative)
        output_path = review / "static/wp-content/uploads" / relative
        if not output_path.is_file():
            errors.append("recovered media for a published source is absent from the local review output")
        elif hashlib.sha256(output_path.read_bytes()).hexdigest() != row.get("sha256"):
            errors.append("recovered media hash changed between retrieval and local review output")
    media_root = review / "static/wp-content/uploads"
    copied_media = {path.relative_to(media_root).as_posix() for path in media_root.rglob("*") if path.is_file()} if media_root.is_dir() else set()
    media_unowned = copied_media - eligible_media
    if media_unowned:
        errors.append(f"{len(media_unowned)} copied media files have no eligible published source owner")
    draft_only_media = copied_media & (excluded_media - eligible_media)
    if draft_only_media:
        errors.append(f"{len(draft_only_media)} copied media files are used only by excluded sources")

    tracked_review_files: list[str] = []
    try:
        result = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True)
        tracked_review_files = [path.decode("utf-8", "replace") for path in result.stdout.split(b"\0") if path.startswith(b"migration-review/")]
    except (OSError, subprocess.CalledProcessError):
        errors.append("could not verify migration-review output is untracked")
    if tracked_review_files:
        errors.append("migration-review output is tracked by Git")

    report = {
        "selection_policy": "post_type in ['post','page'] AND post_status == 'publish' AND post_password == ''",
        "audit_passed": not errors,
        "source_post_page_rows": len(content),
        "eligible_public_published_count": len(eligible),
        "verified_live_only_public_source_count": len(live_sources),
        "migrated_review_count": len(records),
        "excluded_source_rows_proven_absent_from_review": sum(excluded_nonpublished.values()) + len(protected),
        "assertion_no_nonpublic_or_protected_source_migrated": not bool(seen & (set(byid) - set(eligible))),
        "excluded_nonpublished_counts_by_type_status": {f"{kind}/{status}": count for (kind, status), count in sorted(excluded_nonpublished.items())},
        "excluded_password_protected_published_count": len(protected),
        "excluded_counts_include_titles_or_content": False,
        "copied_review_media_count": len(copied_media),
        "media_used_by_eligible_sources_count": len(eligible_media),
        "draft_only_media_copied_count": len(draft_only_media),
        "assertion_draft_only_media_not_copied": not bool(draft_only_media),
        "tracked_review_output_files": len(tracked_review_files),
        "migrated_sources": records,
        "errors": errors,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Source audit: {'PASS' if not errors else 'FAIL'}; migrated={len(records)}; excluded_nonpublished={sum(excluded_nonpublished.values())}; protected={len(protected)}; review_media={len(copied_media)}; draft_only_media={len(draft_only_media)}")
    for error in errors:
        print("FAIL:", error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
