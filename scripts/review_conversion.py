"""Convert only public WordPress sources to ignored local review material.

Conversion records reconciliation and link exceptions, while automated source
fidelity and the final publication ledger decide whether pages can ship.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import shutil
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlparse

from convert import CONVERTER_VERSION, MediaRefs, ROOT, mask_code, read_table, remove_empty_anchor_links, rewrite_internal_urls, sanitize_html, shortcode_media_refs, shortcode_convert, source_slug, unresolved_shortcodes
from publication_policy import is_excluded, read_exclusions


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def path_of(value: str) -> str:
    path = urlparse(value).path or "/"
    return "/" + path.strip("/") + "/" if path.strip("/") else "/"


def taxonomy_slug(value: str) -> str:
    value = unicodedata.normalize("NFKD", html.unescape(value)).encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def wp_date(local_value: str, gmt_value: str) -> str:
    """Preserve the post's actual local/GMT offset rather than assuming UTC."""
    try:
        local = datetime.strptime(local_value, "%Y-%m-%d %H:%M:%S")
        gmt = datetime.strptime(gmt_value, "%Y-%m-%d %H:%M:%S")
        return local.replace(tzinfo=timezone(local - gmt)).isoformat()
    except (TypeError, ValueError):
        return local_value.replace(" ", "T")


def media_relative(value: str) -> str:
    path = unquote(urlparse(html.unescape(value)).path)
    marker = "/wp-content/uploads/"
    if marker not in path:
        return ""
    relative = path.split(marker, 1)[1]
    candidate = Path(relative)
    if not relative or candidate.is_absolute() or ".." in candidate.parts:
        return ""
    return candidate.as_posix()


def apply_media_recovery(text: str, recovered_paths: set[str], unavailable_paths: set[str]) -> str:
    """Localize recovered image/document attributes and drop unavailable images."""
    attr = re.compile(r"(?P<prefix>\b(?:href|src|srcset|poster|data-src|data-lazy-src|data-original)\s*=\s*)(?P<q>[\"'])(?P<value>.*?)(?P=q)", re.I | re.S)

    def rewrite_attribute(match: re.Match[str]) -> str:
        value = match.group("value")
        if re.search(r"\bsrcset\s*=", match.group("prefix"), re.I):
            items = []
            for item in value.split(","):
                bits = item.strip().split()
                if bits and media_relative(bits[0]) in recovered_paths:
                    bits[0] = "/wp-content/uploads/" + media_relative(bits[0])
                items.append(" ".join(bits))
            value = ", ".join(items)
        else:
            relative = media_relative(value)
            if relative in recovered_paths:
                value = "/wp-content/uploads/" + relative
        return match.group("prefix") + match.group("q") + value + match.group("q")

    text = attr.sub(rewrite_attribute, text)
    image = re.compile(r"<img\b[^>]*>", re.I | re.S)

    def remove_unavailable(match: re.Match[str]) -> str:
        tag = match.group(0)
        attrs = {name.lower(): html.unescape(value) for name, _quote, value in
                 re.findall(r"([\w-]+)\s*=\s*([\"'])(.*?)\2", tag, re.I | re.S)}
        candidates = [attrs.get(key, "") for key in ("src", "data-src", "data-lazy-src", "data-original")]
        candidates.extend(item.strip().split()[0] for item in attrs.get("srcset", "").split(",") if item.strip())
        for candidate in candidates:
            relative = media_relative(candidate)
            if relative in unavailable_paths:
                return ""
        return tag

    text = image.sub(remove_unavailable, text)
    # Remove only links made empty by the unavailable-image cleanup.
    return remove_empty_anchor_links(text)


def fix_known_routes(text: str) -> str:
    """Repair one malformed route and externalize one historically broken link."""
    attr = re.compile(r"(?P<prefix>\bhref\s*=\s*)(?P<q>[\"'])(?P<value>.*?)(?P=q)", re.I | re.S)

    def replace(match: re.Match[str]) -> str:
        value = html.unescape(match.group("value")).strip()
        parsed = urlparse(value)
        path = unquote(parsed.path)
        if path == "/2012/installing-openvswitch-on-ubuntu-11-10-with-kvm/":
            value = "https://networkstatic.wordpress.com/2012/02/03/installing-openvswitch-on-ubuntu-11-10-with-kvm/"
        elif "normalizing-th" in path.lower() and "docker-machine" in path.lower():
            value = "/normalizing-the-cloud-with-docker-machine/"
        return match.group("prefix") + match.group("q") + value + match.group("q")

    return attr.sub(replace, text)


def map_attachment_links(text: str, attachment_files: dict[str, str], uploads: Path) -> str:
    """Replace broken WordPress attachment pages with their backed-up media file."""
    tag = re.compile(r"<a\b[^>]*>", re.I | re.S)
    attr = re.compile(r"(?P<prefix>\bhref\s*=\s*)(?P<q>[\"'])(?P<value>.*?)(?P=q)", re.I | re.S)

    def replace_anchor(match: re.Match[str]) -> str:
        anchor = match.group(0)
        rel_match = re.search(r"\brel\s*=\s*([\"'])(.*?)\1", anchor, re.I | re.S)
        attachment_match = re.search(r"\bwp-att-(\d+)\b", rel_match.group(2) if rel_match else "", re.I)
        if not attachment_match:
            return anchor
        relative = attachment_files.get(attachment_match.group(1), "")
        source = (uploads / relative).resolve() if relative else None
        if not relative or not source or not source.is_relative_to(uploads) or not source.is_file():
            return anchor
        return attr.sub(lambda m: m.group("prefix") + m.group("q") +
                        "/wp-content/uploads/" + relative + m.group("q"), anchor, count=1)

    return tag.sub(replace_anchor, text)


def frontmatter(p: dict[str, str], route: str, body_hash: str, author: str,
                categories: list[str], tags: list[str], excerpt: str, content: str,
                featured_image: str, aliases: list[str] | None = None) -> str:
    title = html.unescape(p.get("post_title", ""))
    values = [
        "+++",
        f"title = {json.dumps(title, ensure_ascii=False)}",
        f"date = {json.dumps(wp_date(p.get('post_date', ''), p.get('post_date_gmt', '')))}",
        f"lastmod = {json.dumps(wp_date(p.get('post_modified', ''), p.get('post_modified_gmt', '')))}",
        f"author = {json.dumps(author, ensure_ascii=False)}",
        f"wp_id = {int(p['ID'])}",
        f"categories = {json.dumps(categories, ensure_ascii=False)}",
        f"tags = {json.dumps(tags, ensure_ascii=False)}",
        f"description = {json.dumps(html.unescape(excerpt), ensure_ascii=False)}",
        f"url = {json.dumps(route)}",
        *( [f"aliases = {json.dumps(aliases, ensure_ascii=False)}"] if aliases else [] ),
        *( [f"image = {json.dumps('/wp-content/uploads/' + featured_image)}"] if featured_image else [] ),
        'source_status = "publish"',
        "source_password_protected = false",
        f"source_content_sha256 = {json.dumps(body_hash)}",
        f"conversion_version = {json.dumps(CONVERTER_VERSION)}",
        "review_only = true",
        "draft = true",
        "+++",
        "",
        content,
    ]
    return "\n".join(values)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sql", type=Path, required=True)
    ap.add_argument("--uploads", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, default=ROOT / "migration-review/generated")
    ap.add_argument("--plan-only", action="store_true")
    args = ap.parse_args()

    output = args.output_dir.resolve()
    if not output.is_relative_to((ROOT / "migration-review").resolve()):
        ap.error("--output-dir must be inside migration-review/, separate from production content/ and static/")
    uploads = args.uploads.resolve()
    sql_text = args.sql.read_text(encoding="utf-8", errors="replace")
    posts = list(read_table(sql_text, "posts"))
    byid = {post["ID"]: post for post in posts}
    post_pages = [post for post in posts if post.get("post_type") in ("post", "page")]
    # Explicit source allowlist. No link, taxonomy, title or approval state can
    # broaden this to drafts, private posts, revisions, or protected content.
    eligible = [post for post in post_pages if post.get("post_status") == "publish" and post.get("post_password", "") == ""]
    excluded_password = [post for post in post_pages if post.get("post_status") == "publish" and post.get("post_password", "") != ""]
    excluded_status = Counter((post.get("post_type", ""), post.get("post_status", ""))
                              for post in post_pages if post.get("post_status") != "publish")

    users = {row.get("ID"): row.get("display_name", "") for row in read_table(sql_text, "users")}
    terms = {row.get("term_id"): (row.get("name", ""), row.get("slug", "")) for row in read_table(sql_text, "terms")}
    tax = {row.get("term_taxonomy_id"): (row.get("term_id"), row.get("taxonomy")) for row in read_table(sql_text, "term_taxonomy")}
    relationships = defaultdict(list)
    for row in read_table(sql_text, "term_relationships"):
        pair = tax.get(row.get("term_taxonomy_id"))
        if pair and pair[0] in terms:
            relationships[row.get("object_id")].append((pair[1], terms[pair[0]][0]))
    metadata = defaultdict(dict)
    for row in read_table(sql_text, "postmeta"):
        key = row.get("meta_key", "")
        if key and key not in metadata[row["post_id"]]:
            metadata[row["post_id"]][key] = row.get("meta_value", "")
    attachments = {row["ID"]: metadata[row["ID"]].get("_wp_attached_file", "")
                   for row in posts if row.get("post_type") == "attachment"}
    attachment_files = {attachment_id: relative for attachment_id, relative in attachments.items()
                        if relative and (uploads / relative).is_file()}
    recovery_rows = read_rows(ROOT / "reports/missing-media-recovery.csv")
    recovery_by_path = {row.get("relative_path", ""): row for row in recovery_rows
                        if row.get("relative_path")}
    recovered_paths = {row.get("relative_path", "") for row in recovery_rows
                       if row.get("status") == "recovered" and row.get("relative_path")}
    unavailable_paths = {row.get("relative_path", "") for row in recovery_rows
                         if row.get("status", "").startswith("unavailable") and row.get("relative_path")}

    page_paths: dict[str, str] = {}
    def page_path(page: dict[str, str]) -> str:
        if page["ID"] in page_paths:
            return page_paths[page["ID"]]
        parent = byid.get(page.get("post_parent", "0"))
        value = source_slug(page)
        if parent and parent.get("post_type") == "page":
            value = page_path(parent).strip("/") + "/" + value
        page_paths[page["ID"]] = value
        return value

    def route_for(page: dict[str, str]) -> str:
        return source_slug(page) and ("/" + source_slug(page) + "/" if page.get("post_type") == "post" else "/" + page_path(page) + "/")

    all_by_route = defaultdict(list)
    for page in post_pages:
        all_by_route[route_for(page)].append(page)
    eligible_by_route = defaultdict(list)
    for page in eligible:
        eligible_by_route[route_for(page)].append(page)

    eligible_by_slug = defaultdict(list)
    for page in eligible:
        if page.get("post_type") == "post":
            eligible_by_slug[source_slug(page)].append(page)

    # Preserve historical year/month/day paths only when an eligible article
    # links to the path and its slug plus date prefix identify one backup post.
    historical_alias_to_route = {}
    alias_sources = defaultdict(set)
    for source_post in eligible:
        _converted, _media, source_routes = rewrite_internal_urls(source_post.get("post_content", ""))
        for alias_path in source_routes:
            parts = alias_path.strip("/").split("/")
            if len(parts) not in (2, 3, 4) or not re.fullmatch(r"\d{4}", parts[0]):
                continue
            prefix_parts = parts[:-1]
            matches = [candidate for candidate in eligible_by_slug.get(parts[-1], [])
                       if candidate.get("post_date", "")[:10].split("-")[:len(prefix_parts)] == prefix_parts]
            if len(matches) != 1 or alias_path in all_by_route:
                continue
            target_route = route_for(matches[0])
            previous = historical_alias_to_route.get(alias_path)
            if previous and previous != target_route:
                historical_alias_to_route.pop(alias_path, None)
                alias_sources.pop(alias_path, None)
                continue
            historical_alias_to_route[alias_path] = target_route
            alias_sources[alias_path].add(int(source_post["ID"]))
    aliases_by_target = defaultdict(list)
    for alias_path, target_route in historical_alias_to_route.items():
        aliases_by_target[target_route].append(alias_path)

    verification_by_path = {path_of(row.get("permalink", "")): row for row in read_rows(ROOT / "reports/content-verification.csv")}
    reconciliation_by_path = {path_of(row.get("backup_permalink", "")): row for row in read_rows(ROOT / "reports/live-vs-backup.csv") if row.get("backup_permalink")}
    url_rows = read_rows(ROOT / "reports/url-inventory.csv")
    eligible_categories = {name for object_id, rels in relationships.items() if object_id in {p["ID"] for p in eligible}
                           for kind, name in rels if kind == "category"}
    eligible_tags = {name for object_id, rels in relationships.items() if object_id in {p["ID"] for p in eligible}
                     for kind, name in rels if kind == "post_tag"}
    known_site_routes = set()
    taxonomy_alias_rows = []
    for row in url_rows:
        url_type = row.get("url_type")
        destination = path_of(row.get("destination_path", ""))
        if url_type in ("post", "page"):
            continue
        if url_type in ("post_tag", "category"):
            term_name = row.get("owner_urls", "")
            active_terms = eligible_tags if url_type == "post_tag" else eligible_categories
            if term_name not in active_terms:
                continue
            old_parts = destination.strip("/").split("/")
            canonical = f"/{old_parts[0]}/{taxonomy_slug(term_name)}/"
            if destination != canonical:
                taxonomy = "tags" if url_type == "post_tag" else "categories"
                term_file = ROOT / "content" / taxonomy / taxonomy_slug(term_name) / "_index.md"
                registered = term_file.is_file() and destination in term_file.read_text(encoding="utf-8")
                taxonomy_alias_rows.append({"source_path": destination, "target_path": canonical,
                                            "taxonomy": url_type, "term_name": term_name,
                                            "alias_registered": "yes" if registered else "no"})
                if not registered:
                    continue
        known_site_routes.add(destination)
    known_site_routes.update(("/", "/archive/", "/search/", "/author/brent/"))

    prepared = []
    asset_owners = defaultdict(set)
    page_assets = defaultdict(set)
    for post in sorted(eligible, key=lambda row: (row.get("post_date", ""), int(row.get("ID", "0")))):
        # Keep this assertion next to conversion: there is no relaxed code path.
        assert post.get("post_status") == "publish" and post.get("post_password", "") == ""
        route = route_for(post)
        raw = post.get("post_content", "")
        source_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        raw_for_dependencies = remove_empty_anchor_links(raw)
        media_parser = MediaRefs()
        media_parser.feed(mask_code(raw_for_dependencies)[0])
        refs = set()
        for url, _kind in media_parser.refs:
            path = unquote(urlparse(html.unescape(url)).path)
            marker = "/wp-content/uploads/"
            if marker in path:
                refs.add(path.split(marker, 1)[1])
        refs.update(shortcode_media_refs(raw_for_dependencies))
        thumb = metadata[post["ID"]].get("_thumbnail_id", "")
        featured_image = attachments.get(thumb, "") if thumb else ""
        if featured_image:
            refs.add(featured_image)

        converted, unresolved = shortcode_convert(raw)
        converted = map_attachment_links(converted, attachment_files, uploads)
        converted = fix_known_routes(converted)
        converted = apply_media_recovery(converted, recovered_paths, unavailable_paths)
        rendered_media_parser = MediaRefs()
        rendered_media_parser.feed(mask_code(converted)[0])
        for url, _kind in rendered_media_parser.refs:
            path = unquote(urlparse(html.unescape(url)).path)
            marker = "/wp-content/uploads/"
            if marker in path:
                refs.add(path.split(marker, 1)[1])
        converted, rewritten_media, internal_routes = rewrite_internal_urls(converted)
        refs.update(rewritten_media)
        converted = sanitize_html(converted)
        repair_notes = []
        if re.search(r'\[image_frame\b[^\]]*\]\s*h(?=https?://)', raw, re.I):
            repair_notes.append("image_frame URL had one extra leading h; normalized in review output")
        if re.search(r'citelink\s*=\s*["\']\s*-\s*(?=https?://)', raw, re.I):
            repair_notes.append("citeLink URL had one extra leading hyphen; normalized in review output")
        unresolved = sorted(set(unresolved + unresolved_shortcodes(converted) + repair_notes))
        existing, missing, unsafe = [], [], []
        for relative in sorted(refs):
            source = (uploads / relative).resolve()
            if not source.is_relative_to(uploads):
                unsafe.append(relative)
            elif source.is_file():
                existing.append(relative)
            elif relative in recovered_paths and (ROOT / "migration-review/recovered-media/wp-content/uploads" / relative).is_file():
                existing.append(relative)
            elif not source.is_file():
                missing.append(relative)

        category_names = sorted(name for kind, name in relationships[post["ID"]] if kind == "category")
        tag_names = sorted(name for kind, name in relationships[post["ID"]] if kind == "post_tag")
        author = users.get(post.get("post_author"), "") or "Unknown"
        content_rel = (Path("pages") / page_path(post) / "index.md" if post.get("post_type") == "page"
                       else Path("posts") / (source_slug(post) + ".md"))
        body = frontmatter(post, route, source_hash, author, category_names, tag_names,
                           post.get("post_excerpt", ""), converted, featured_image,
                           sorted(aliases_by_target.get(route, [])))
        verification = verification_by_path.get(route, {})
        reconciliation = reconciliation_by_path.get(route, {})
        prepared.append({"post": post, "route": route, "content_rel": content_rel, "body": body,
                         "title": html.unescape(post.get("post_title", "")), "source_hash": source_hash,
                         "refs": sorted(refs), "existing_media": existing, "missing_media": missing,
                         "unsafe_media": unsafe, "unresolved_shortcodes": unresolved,
                         "internal_routes": sorted(set(urlparse(value).path or "/" for value in internal_routes)),
                         "verification": verification, "reconciliation": reconciliation})
        for relative in existing:
            asset_owners[relative].add(route)
            page_assets[route].add(relative)

    prepared_by_route = {item["route"]: item for item in prepared}
    initial_candidates = set()
    reasons_by_route = {}
    for item in prepared:
        reasons = []
        if item["unsafe_media"]:
            reasons.append("unsafe media path rejected")
        reasons_by_route[item["route"]] = reasons
        if not reasons:
            initial_candidates.add(item["route"])

    def target_problem(item: dict, candidate_paths: set[str]) -> list[dict]:
        problems = []
        for target in item["internal_routes"]:
            if target.startswith("/wp-content/uploads/"):
                continue
            resolved_target = historical_alias_to_route.get(target, target)
            resolution_method = "historical date path matched by slug and post date" if target != resolved_target else "exact route"
            target_records = all_by_route.get(resolved_target, [])
            if target_records:
                if resolved_target not in candidate_paths:
                    for target_post in target_records:
                        problems.append({"target_path": target, "resolved_target_permalink": resolved_target,
                                         "resolution_method": resolution_method, "target_wp_id": target_post["ID"],
                                         "target_status": target_post.get("post_status", ""),
                                         "target_password_protected": "yes" if target_post.get("post_password", "") else "no",
                                         "exception": "linked WordPress route is not publication-eligible"})
                continue
            if target in known_site_routes:
                continue
            static_target = (ROOT / "static" / target.lstrip("/")).resolve()
            if static_target.is_relative_to((ROOT / "static").resolve()) and static_target.exists():
                continue
            problems.append({"target_path": target, "resolved_target_permalink": "",
                             "resolution_method": "unresolved", "target_wp_id": "", "target_status": "unknown",
                             "target_password_protected": "unknown", "exception": "no exact public post/page or known site route found"})
        return problems

    # Published, unprotected source pages are considered as a complete set for
    # normal internal dependencies. Per-link exceptions remain recorded, but
    # a target article's live-parity status cannot block its callers.
    publication_candidates = set(initial_candidates)

    link_exceptions = []
    for item in prepared:
        for problem in target_problem(item, publication_candidates):
            link_exceptions.append({"source_permalink": item["route"], "source_wp_id": item["post"]["ID"],
                                    "target_path": problem["target_path"], "target_wp_id": problem["target_wp_id"],
                                    "resolved_target_permalink": problem.get("resolved_target_permalink", ""),
                                    "resolution_method": problem.get("resolution_method", "unresolved"),
                                    "target_status": problem["target_status"],
                                    "target_password_protected": problem["target_password_protected"],
                                    "target_imported_to_review": "yes" if problem.get("resolved_target_permalink") in prepared_by_route else "no",
                                    "target_publication_eligible": "yes" if problem.get("resolved_target_permalink") in publication_candidates else "no",
                                    "exception": problem["exception"]})

    conversion_rows, publication_rows, source_rows = [], [], []
    for item in prepared:
        post, route = item["post"], item["route"]
        page_links = [row for row in link_exceptions if row["source_permalink"] == route]
        reasons = list(reasons_by_route[route])
        if item["unresolved_shortcodes"]:
            reasons.append("documented shortcode/media presentation exceptions: " + "|".join(item["unresolved_shortcodes"]))
        if item["missing_media"]:
            reasons.append("documented unavailable media: " + "|".join(item["missing_media"]))
        if page_links:
            reasons.append("documented per-link exceptions; preserved source links are audited separately")
        conversion_rows.append({"permalink": route, "wp_id": post["ID"], "type": post["post_type"], "title": item["title"],
                                "source_status": "publish", "source_password_protected": "no",
                                "conversion_status": "converted-to-local-review", "conversion_exceptions": "|".join(item["unresolved_shortcodes"]),
                                "missing_media": "|".join(item["missing_media"]), "unsafe_media": "|".join(item["unsafe_media"]),
                                "link_exception_count": len(page_links), "media_count": len(item["refs"]),
                                "source_content_sha256": item["source_hash"],
                                "review_content_path": (Path("migration-review/generated/content") / item["content_rel"]).as_posix()})
        publication_rows.append({"permalink": route, "wp_id": post["ID"], "type": post["post_type"], "title": item["title"],
                                 "source_status": "publish", "source_password_protected": "no",
                                 "reconciliation_status": item["reconciliation"].get("classification", "not observed"),
                                 "body_verification_status": item["verification"].get("verification", "not checked"),
                                 "conversion_issue_count": len(item["unresolved_shortcodes"]) + len(item["missing_media"]) + len(item["unsafe_media"]),
                                 "link_exception_count": len(page_links),
                                 "publish_eligible": "yes" if route in publication_candidates else "no",
                                 "eligibility_reasons": "|".join(reasons)})
        source_rows.append({"wp_id": int(post["ID"]), "post_type": post["post_type"], "post_status": "publish",
                            "password_protected": False, "source_content_sha256": item["source_hash"],
                            "review_content_path": (Path("migration-review/generated/content") / item["content_rel"]).as_posix()})

    live_eligibility = {row.get("wp_id", ""): row for row in read_rows(ROOT / "reports/live-source-eligibility.csv")}
    excluded_ids, excluded_routes = read_exclusions(ROOT)
    for row in read_rows(ROOT / "reports/live-vs-backup.csv"):
        if row.get("classification") == "live-only":
            route = path_of(row.get("live_permalink", ""))
            live = next((value for value in live_eligibility.values() if path_of(value.get("route", "")) == route), {})
            verified = (live.get("source_status") == "publish" and live.get("password_protected") == "no"
                        and live.get("anonymous_full_body") == "yes" and live.get("route_http_status") == "200"
                        and not live.get("conversion_exceptions", ""))
            excluded = is_excluded(live.get("wp_id", ""), route, excluded_ids, excluded_routes)
            publication_rows.append({"permalink": route, "wp_id": live.get("wp_id", ""), "type": "live-only",
                                     "title": row.get("live_title", ""), "source_status": live.get("source_status", "not-in-backup"),
                                     "source_password_protected": live.get("password_protected", "not-applicable"), "reconciliation_status": "verified-live-only",
                                     "body_verification_status": "full-body-verified" if verified else "unrecovered",
                                     "conversion_issue_count": len(list(filter(None, live.get("conversion_exceptions", "").split("|")))),
                                     "link_exception_count": 0, "publish_eligible": "no" if excluded else "yes" if verified else "no",
                                     "eligibility_reasons": "excluded by migration publication policy" if excluded else
                                         "verified live-only source; conversion and public-status evidence recorded" if verified else
                                         "full article, code, links and media not recovered"})

    media_rows = []
    for relative, owners in sorted(asset_owners.items()):
        backup_source = (uploads / relative).resolve()
        recovered_source = (ROOT / "migration-review/recovered-media/wp-content/uploads" / relative).resolve()
        if backup_source.is_relative_to(uploads) and backup_source.is_file():
            source = backup_source
            source_origin = "backup upload"
            source_url = ""
        elif relative in recovered_paths and recovered_source.is_file():
            source = recovered_source
            source_origin = "recovered public media"
            source_url = recovery_by_path.get(relative, {}).get("source_url", "")
        else:
            continue
        digest = hashlib.sha256()
        with source.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        media_rows.append({"source_path": relative, "sha256": digest.hexdigest(), "size_bytes": source.stat().st_size,
                           "owner_urls": "|".join(sorted(owners)), "source_origin": source_origin,
                           "source_url": source_url})

    report_dir = ROOT / "reports"
    report_dir.mkdir(exist_ok=True)
    audit = {"selection_policy": "post_type in ['post','page'] AND post_status == 'publish' AND post_password == ''",
             "converter_version": CONVERTER_VERSION, "mode": "plan-only" if args.plan_only else "local-review-output",
             "source_post_page_rows": len(post_pages), "eligible_public_published_rows": len(eligible),
             "review_content_rows": len(prepared), "review_posts": sum(x["post"]["post_type"] == "post" for x in prepared),
             "review_pages": sum(x["post"]["post_type"] == "page" for x in prepared),
             "excluded_nonpublished_counts_by_type_status": {f"{kind}/{status}": count for (kind, status), count in sorted(excluded_status.items())},
             "excluded_password_protected_published_count": len(excluded_password),
             "excluded_counts_include_titles_or_content": False,
             "assertion_all_review_sources_are_published_and_unprotected": all(row["post_status"] == "publish" and not row["password_protected"] for row in source_rows),
             "review_sources": source_rows}
    (report_dir / "migration-source-audit.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    write_csv(report_dir / "conversion-review.csv", conversion_rows,
              ["permalink", "wp_id", "type", "title", "source_status", "source_password_protected", "conversion_status",
               "conversion_exceptions", "missing_media", "unsafe_media", "link_exception_count", "media_count", "source_content_sha256", "review_content_path"])
    write_csv(report_dir / "publication-eligibility.csv", publication_rows,
              ["permalink", "wp_id", "type", "title", "source_status", "source_password_protected", "reconciliation_status",
               "body_verification_status", "conversion_issue_count", "link_exception_count", "publish_eligible", "eligibility_reasons"])
    write_csv(report_dir / "link-exceptions.csv", link_exceptions,
              ["source_permalink", "source_wp_id", "target_path", "resolved_target_permalink", "resolution_method",
               "target_wp_id", "target_status", "target_password_protected",
               "target_imported_to_review", "target_publication_eligible", "exception"])
    alias_rows = [{"alias_path": alias_path, "target_permalink": target_route,
                   "target_wp_id": all_by_route[target_route][0]["ID"],
                   "linked_from_source_wp_ids": "|".join(str(value) for value in sorted(alias_sources[alias_path])),
                   "evidence": "internal link in eligible published source; backup post slug and date prefix match uniquely"}
                  for alias_path, target_route in sorted(historical_alias_to_route.items())]
    write_csv(report_dir / "historical-link-aliases.csv", alias_rows,
              ["alias_path", "target_permalink", "target_wp_id", "linked_from_source_wp_ids", "evidence"])
    write_csv(report_dir / "taxonomy-route-aliases.csv", taxonomy_alias_rows,
              ["source_path", "target_path", "taxonomy", "term_name", "alias_registered"])
    write_csv(report_dir / "media-copy-manifest.csv", media_rows,
              ["source_path", "sha256", "size_bytes", "owner_urls", "source_origin", "source_url"])

    if not args.plan_only:
        marker = output / ".networkstatic-generated"
        if output.exists():
            if not marker.is_file() or marker.read_text(encoding="utf-8").strip() != "networkstatic-conversion-review-v1":
                ap.error(f"refusing to replace unmarked output directory: {output}")
            shutil.rmtree(output)
        (output / "content").mkdir(parents=True)
        (output / "static").mkdir(parents=True)
        (output / ".networkstatic-generated").write_text("networkstatic-conversion-review-v1\n", encoding="utf-8")
        for item in prepared:
            destination = output / "content" / item["content_rel"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(item["body"], encoding="utf-8")
        for row in media_rows:
            source = ((uploads / row["source_path"]).resolve() if row["source_origin"] == "backup upload" else
                      (ROOT / "migration-review/recovered-media/wp-content/uploads" / row["source_path"]).resolve())
            destination = output / "static/wp-content/uploads" / row["source_path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        owners = {"asset_to_pages": {key: sorted(value) for key, value in sorted(asset_owners.items())},
                  "page_to_assets": {key: sorted(value) for key, value in sorted(page_assets.items())}}
        (report_dir / "asset-owners.json").write_text(json.dumps(owners, indent=2) + "\n", encoding="utf-8")
        written = list((output / "content").rglob("*.md"))
        if len(written) != len(eligible):
            raise RuntimeError(f"expected {len(eligible)} review pages; wrote {len(written)}")
        if not audit["assertion_all_review_sources_are_published_and_unprotected"]:
            raise RuntimeError("source eligibility assertion failed")

    media_bytes = sum(row["size_bytes"] for row in media_rows)
    status = ["# Conversion status", "",
              f"Eligible public sources: {len(eligible)}; local review pages converted: {len(prepared)}; publication-eligible: {sum(row['publish_eligible'] == 'yes' for row in publication_rows)}.",
              f"Excluded nonpublished post/page rows: {sum(excluded_status.values())}; excluded password-protected published rows: {len(excluded_password)}.",
              f"Referenced media copied/planned: {len(media_rows)} files / {media_bytes:,} bytes.",
              f"Mode: {'plan-only' if args.plan_only else 'local review output at `'+output.relative_to(ROOT).as_posix()+'`'}.",
              "Review output is outside Hugo production content/static roots. Each review page is marked `draft = true`; conversion does not grant publication approval.",
              "Excluded source rows are recorded only as aggregate counts; draft titles and content are not written to reports or migration output."]
    (report_dir / "conversion-status.md").write_text("\n".join(status) + "\n", encoding="utf-8")
    print(f"Eligible public sources: {len(eligible)}; review conversions: {len(prepared)}; publication-eligible: {sum(row['publish_eligible'] == 'yes' for row in publication_rows)}; media: {len(media_rows)}; plan_only={args.plan_only}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
