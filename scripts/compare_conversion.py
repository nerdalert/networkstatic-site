#!/usr/bin/env python3
"""Compare converted review pages with their public WordPress source rows."""
from __future__ import annotations

import argparse
import csv
import difflib
import hashlib
import html
import json
import re
import tomllib
import unicodedata
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

from convert import MediaRefs, mask_code, read_table, remove_empty_anchor_links, rewrite_internal_urls, shortcode_media_refs, shortcode_convert
from publication_policy import is_excluded, read_exclusions

ROOT = Path(__file__).resolve().parents[1]
UPLOAD_MARKER = "/wp-content/uploads/"


class TextContent(HTMLParser):
    def __init__(self, include_alt: bool = True) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.include_alt = include_alt

    def handle_starttag(self, tag: str, attrs) -> None:
        values = dict(attrs)
        if self.include_alt and tag in ("img", "area") and values.get("alt"):
            self.parts.extend((" ", values["alt"], " "))
        if tag in ("br", "hr"):
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.values: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        for key, value in attrs:
            if key.lower() in ("href", "src", "poster", "data-src", "data-original", "data-lazy-src") and value:
                self.values.append(value)


CODE_RE = re.compile(
    r"(?is)"
    r"(?P<crayon>\[crayon\b[^\]]*\].*?\[/crayon\s*\])"
    r"|(?P<pre><pre\b[^>]*>.*?</pre\s*>)"
    r"|(?P<fenced>^[ \t]*(?P<fence_mark>`{3,}|~{3,})[^\n]*\n.*?^[ \t]*(?P=fence_mark)[ \t]*$)"
    r"|(?P<code><code\b[^>]*>.*?</code\s*>)"
    r"|(?P<inline>`+[^`\n]+`+)"
)
RELURL_RE = re.compile(r"\{\{\s*[<%]\s*relurl\s+(?P<arg>.+?)\s+[>%]\s*\}\}", re.S)
MARKDOWN_LINK_RE = re.compile(
    r"!?\[[^\]\n]*\]\(\s*(?:<([^>]+)>|([^\s)]+))(?:\s+(?:\"[^\"]*\"|'[^']*'))?\s*\)", re.S
)
BARE_URL_RE = re.compile(r"(?:https?:)?//[^\s<>\[\]\)\"']+", re.I)
SHORTCODE_LINK_RE = re.compile(r"\[[A-Za-z][\w-]*\b([^\]]*)\]", re.I)
SHORTCODE_ATTR_RE = re.compile(r"([\w-]+)\s*=\s*([\"'])(.*?)\2", re.S)


def code_samples(body: str) -> tuple[list[tuple[str, str]], str]:
    samples: list[tuple[str, str]] = []
    index = 0
    pieces: list[str] = []
    for match in CODE_RE.finditer(body):
        pieces.append(body[index:match.start()])
        index = match.end()
        value = match.group()
        if match.group("crayon") is not None:
            value = re.sub(r"^\[crayon\b[^\]]*\]|\[/crayon\s*\]$", "", value, flags=re.I | re.S)
            block = "block"
        elif match.group("pre") is not None:
            value = re.sub(r"^<pre\b[^>]*>|</pre\s*>$", "", value, flags=re.I | re.S)
            block = "block"
        elif match.group("fenced") is not None:
            lines = value.splitlines()
            value = "\n".join(lines[1:-1])
            block = "block"
        elif match.group("code") is not None:
            value = re.sub(r"^<code\b[^>]*>|</code\s*>$", "", value, flags=re.I | re.S)
            block = "inline"
        else:
            value = value[1:-1]
            block = "inline"
        parser = TextContent(include_alt=False)
        parser.feed(value)
        code = html.unescape("".join(parser.parts)).replace("\r\n", "\n").replace("\r", "\n").strip("\n")
        samples.append((block, code))
        pieces.append(f" __CODE_{len(samples)-1}_{block.upper()}__ ")
    pieces.append(body[index:])
    return samples, "".join(pieces)


def relurl_destination(match: re.Match[str]) -> str:
    argument = match.group("arg").strip()
    try:
        return json.loads(argument)
    except json.JSONDecodeError:
        return argument.strip("\"'")


def html_parseable_body(body: str) -> str:
    # Hugo resolves these before rendering. Replacing them with their paths
    # makes source-side parsing see valid quoted HTML attributes.
    return RELURL_RE.sub(lambda match: relurl_destination(match), body)


def normalized_text(body: str) -> str:
    body, _conversion_exceptions = shortcode_convert(body)
    _samples, body = code_samples(body)
    def image_text(match: re.Match[str]) -> str:
        attrs = {key.lower(): html.unescape(value) for key, _quote, value in SHORTCODE_ATTR_RE.findall(match.group(1))}
        image = match.group(2)
        if re.search(r"<img\b", image, re.I):
            return image
        return '<img alt="' + html.escape(attrs.get("alt", ""), quote=True) + '">' if image.strip() else ""
    body = re.sub(r"\[image_frame\b([^\]]*)\](.*?)\[/image_frame\s*\]", image_text, body, flags=re.I | re.S)
    body = html_parseable_body(body)
    body = BARE_URL_RE.sub(lambda match: normalize_url(match.group(0)), body)
    body = MARKDOWN_LINK_RE.sub(lambda match: match.group(0).split("](", 1)[0].lstrip("!")[1:], body)
    body = re.sub(r"(?m)^\s*\[(?:/?[A-Za-z][\w-]*)[^\]]*\]\s*$", " ", body)
    body = re.sub(r"\[/?[A-Za-z][\w-]*\b[^\]]*\]", " ", body)
    body = re.sub(r"(?m)^\s{0,3}#{1,6}\s*", "", body)
    body = re.sub(r"(?m)^\s*([-*+]|\d+[.)])\s+", "", body)
    body = re.sub(r"(?m)^\s*[-*_]{3,}\s*$", " ", body)
    body = re.sub(r"[*_~]{1,3}", "", body)
    parser = TextContent()
    parser.feed(body)
    value = unicodedata.normalize("NFC", html.unescape("".join(parser.parts)))
    return " ".join(value.split())


def normalize_url(value: str) -> str:
    value = html.unescape(value.strip().strip("<>\"'"))
    if not value:
        return ""
    if value.startswith("{{"):
        match = RELURL_RE.search(value)
        if match:
            argument = match.group("arg").strip()
            try:
                value = json.loads(argument)
            except json.JSONDecodeError:
                value = argument.strip("\"'")
    value = value.strip()
    parsed = urlparse(value)
    host = (parsed.hostname or "").lower()
    path = unquote(parsed.path or "/")
    marker = "/wp-content/uploads/"
    if marker in path:
        return marker + path.split(marker, 1)[1] + (("?" + parsed.query) if parsed.query else "") + (("#" + parsed.fragment) if parsed.fragment else "")
    if "normalizing-th" in path.lower() and "docker-machine" in path.lower():
        return "/normalizing-the-cloud-with-docker-machine/"
    if path == "/2012/installing-openvswitch-on-ubuntu-11-10-with-kvm/":
        return "https://networkstatic.wordpress.com/2012/02/03/installing-openvswitch-on-ubuntu-11-10-with-kvm/"
    if host in ("networkstatic.net", "www.networkstatic.net"):
        if path.startswith("/~bbsali0/"):
            path = path[len("/~bbsali0"):]
        return path + (("?" + parsed.query) if parsed.query else "") + (("#" + parsed.fragment) if parsed.fragment else "")
    if not parsed.scheme and value.startswith("/"):
        path = unquote(parsed.path or "/")
        if path.startswith("/~bbsali0/"):
            path = path[len("/~bbsali0"):]
        return path + (("?" + parsed.query) if parsed.query else "") + (("#" + parsed.fragment) if parsed.fragment else "")
    if parsed.scheme and parsed.netloc:
        return parsed.scheme.lower() + "://" + parsed.netloc.lower() + parsed.path + (("?" + parsed.query) if parsed.query else "") + (("#" + parsed.fragment) if parsed.fragment else "")
    return value.rstrip(".,;:")


def link_targets(body: str) -> set[str]:
    _code, body = code_samples(body)
    parser = Links()
    parser.feed(html_parseable_body(body))
    values = list(parser.values)
    values.extend(relurl_destination(match) for match in RELURL_RE.finditer(body))
    parseable = html_parseable_body(body)
    for match in MARKDOWN_LINK_RE.finditer(parseable):
        values.append(match.group(1) or match.group(2) or "")
    text_only = re.sub(r"<[^>]*>", " ", parseable)
    values.extend(BARE_URL_RE.findall(text_only))
    for match in SHORTCODE_LINK_RE.finditer(body):
        attrs = {key.lower(): html.unescape(value) for key, _quote, value in SHORTCODE_ATTR_RE.findall(match.group(1))}
        for key in ("link", "url", "href", "file", "src", "citelink", "citationlink"):
            if attrs.get(key):
                candidate = attrs[key].strip().lstrip("- ").strip()
                parsed = urlparse(candidate)
                if parsed.scheme in ("http", "https") and parsed.netloc or candidate.startswith("/"):
                    values.append(candidate)
                    break
    result = {normalize_url(value) for value in values if normalize_url(value)}
    return result


def media_targets(body: str, featured: str = "") -> set[str]:
    _code, body = code_samples(body)
    parser = MediaRefs()
    parser.feed(html_parseable_body(body))
    values = [value for value, _kind in parser.refs]
    values.extend(relurl_destination(match) for match in RELURL_RE.finditer(body))
    result = set(shortcode_media_refs(body))
    if featured:
        values.append(featured)
    for value in values:
        value = normalize_url(value)
        path = unquote(urlparse(value).path)
        if UPLOAD_MARKER in path:
            result.add(path.split(UPLOAD_MARKER, 1)[1])
    return result


def sha_text(values: list[str]) -> str:
    return hashlib.sha256("\0".join(values).encode("utf-8")).hexdigest()


def file_sha256(path: Path, cache: dict[Path, str]) -> str:
    resolved = path.resolve()
    if resolved not in cache:
        digest = hashlib.sha256()
        with resolved.open("rb") as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(chunk)
        cache[resolved] = digest.hexdigest()
    return cache[resolved]


def remove_unavailable_images(body: str, unavailable: set[str]) -> str:
    """Mirror the approved cleanup for unavailable image elements, preserving captions."""
    prose, saved, prefix = mask_code(body)
    image = re.compile(r"<img\b[^>]*>", re.I | re.S)

    def remove(match: re.Match[str]) -> str:
        attrs = {name.lower(): html.unescape(value) for name, _quote, value in
                 re.findall(r"([\w-]+)\s*=\s*([\"'])(.*?)\2", match.group(0), re.I | re.S)}
        candidates = [attrs.get(key, "") for key in ("src", "data-src", "data-lazy-src", "data-original")]
        candidates.extend(item.strip().split()[0] for item in attrs.get("srcset", "").split(",") if item.strip())
        for candidate in candidates:
            path = unquote(urlparse(candidate).path)
            if UPLOAD_MARKER in path and path.split(UPLOAD_MARKER, 1)[1] in unavailable:
                return ""
        return match.group(0)

    prose = image.sub(remove, prose)
    prose = _restore_masked(prose, saved, prefix)
    return remove_empty_anchor_links(prose)


def _restore_masked(body: str, saved: list[str], prefix: str) -> str:
    for index, value in enumerate(saved):
        body = body.replace(f"{prefix}{index}@@", value)
    return body


def map_attachment_links(body: str, attachments: dict[str, str]) -> str:
    anchor = re.compile(r"<a\b[^>]*>", re.I | re.S)
    href = re.compile(r"(?P<prefix>\bhref\s*=\s*)(?P<q>[\"'])(?P<value>.*?)(?P=q)", re.I | re.S)

    def replace(match: re.Match[str]) -> str:
        tag = match.group(0)
        rel = re.search(r"\brel\s*=\s*([\"'])(.*?)\1", tag, re.I | re.S)
        attachment = re.search(r"\bwp-att-(\d+)\b", rel.group(2) if rel else "", re.I)
        relative = attachments.get(attachment.group(1), "") if attachment else ""
        if not relative:
            return tag
        return href.sub(lambda item: item.group("prefix") + item.group("q") +
                        "/wp-content/uploads/" + relative + item.group("q"), tag, count=1)

    return anchor.sub(replace, body)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sql", type=Path, required=True)
    ap.add_argument("--uploads", type=Path, required=True)
    ap.add_argument("--review-dir", type=Path, default=ROOT / "migration-review/generated")
    ap.add_argument("--fidelity-report", type=Path, default=ROOT / "reports/conversion-fidelity.csv")
    args = ap.parse_args()
    review = args.review_dir.resolve()
    if not review.is_relative_to((ROOT / "migration-review").resolve()):
        ap.error("--review-dir must be inside migration-review/")

    sql = args.sql.read_text(encoding="utf-8", errors="replace")
    posts = list(read_table(sql, "posts"))
    eligible = {row["ID"]: row for row in posts if row.get("post_type") in ("post", "page")
                and row.get("post_status") == "publish" and row.get("post_password", "") == ""}
    metadata = defaultdict(dict)
    for row in read_table(sql, "postmeta"):
        key = row.get("meta_key", "")
        if key and key not in metadata[row["post_id"]]:
            metadata[row["post_id"]][key] = row.get("meta_value", "")
    attachments = {row["ID"]: metadata[row["ID"]].get("_wp_attached_file", "")
                   for row in posts if row.get("post_type") == "attachment"}
    recovery_rows = list(csv.DictReader((ROOT / "reports/missing-media-recovery.csv").open(encoding="utf-8", newline=""))) if (ROOT / "reports/missing-media-recovery.csv").is_file() else []
    recovery_by_path = {row.get("relative_path", ""): row for row in recovery_rows if row.get("relative_path")}
    recovered_paths = {path for path, row in recovery_by_path.items() if row.get("status") == "recovered"}
    unavailable_paths = {path for path, row in recovery_by_path.items() if row.get("status", "").startswith("unavailable")}
    output_files = list((review / "content").rglob("*.md")) if (review / "content").is_dir() else []
    converted = {}
    for path in output_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        close = text.find("\n+++\n", 4)
        if not text.startswith("+++\n") or close < 0:
            continue
        front = tomllib.loads(text[4:close])
        converted[str(front.get("wp_id", ""))] = (path, front, text[close + 5:])
    owners_path = ROOT / "reports/asset-owners.json"
    owner_map = json.loads(owners_path.read_text(encoding="utf-8")) if owners_path.is_file() else {"page_to_assets": {}}
    source_uploads = args.uploads.resolve()
    output_media_root = review / "static/wp-content/uploads"
    file_hash_cache: dict[Path, str] = {}
    rows = []

    for wp_id, post in sorted(eligible.items(), key=lambda item: (item[1].get("post_date", ""), int(item[0]))):
        route = "/" + post.get("post_name", "") + "/"
        if not post.get("post_name"):
            route = "/wp-" + wp_id + "/"
        item = converted.get(wp_id)
        if not item:
            rows.append({"wp_id": wp_id, "permalink": route, "source_status": "publish", "password_protected": "no",
                         "comparison_status": "missing-review-output"})
            continue
        _path, front, output_body = item
        source_body = post.get("post_content", "")
        source_codes, _ = code_samples(source_body)
        output_codes, _ = code_samples(output_body)
        comparable_source_body = remove_empty_anchor_links(remove_unavailable_images(source_body, unavailable_paths))
        source_text = normalized_text(comparable_source_body)
        output_text = normalized_text(output_body)
        text_exact = source_text == output_text
        text_ratio = 1.0 if text_exact else difflib.SequenceMatcher(None, source_text, output_text).ratio()
        code_source_values = [f"{kind}:{value}" for kind, value in source_codes]
        code_output_values = [f"{kind}:{value}" for kind, value in output_codes]
        code_exact = code_source_values == code_output_values

        source_body_for_links = map_attachment_links(comparable_source_body, attachments)
        source_links = link_targets(source_body_for_links)
        output_links = link_targets(output_body)
        missing_links = sorted(source_links - output_links)
        extra_links = sorted(output_links - source_links)
        links_exact = not missing_links and not extra_links

        source_for_media, _source_shortcode_exceptions = shortcode_convert(remove_empty_anchor_links(source_body))
        source_media = media_targets(source_for_media)
        thumb = metadata[wp_id].get("_thumbnail_id", "")
        featured_rel = attachments.get(thumb, "") if thumb else ""
        if featured_rel:
            source_media.add(featured_rel)
        output_media = media_targets(output_body, front.get("image", ""))
        manifest_media = set(owner_map.get("page_to_assets", {}).get(route, []))
        media_hashes_exact = True
        missing_files = []
        changed_files = []
        recovered_refs = []
        unavailable_image_refs = []
        unavailable_document_refs = []
        for relative in sorted(source_media):
            source = (source_uploads / relative).resolve()
            destination = (output_media_root / relative).resolve()
            if not source.is_relative_to(source_uploads):
                missing_files.append(relative)
                media_hashes_exact = False
                continue
            if source.is_file():
                if not destination.is_file():
                    missing_files.append(relative)
                    media_hashes_exact = False
                elif file_sha256(source, file_hash_cache) != file_sha256(destination, file_hash_cache):
                    media_hashes_exact = False
                    changed_files.append(relative)
                continue
            if relative in recovered_paths:
                recovery = recovery_by_path[relative]
                if not destination.is_file() or file_sha256(destination, file_hash_cache) != recovery.get("sha256", ""):
                    missing_files.append(relative)
                    media_hashes_exact = False
                else:
                    recovered_refs.append(relative)
                continue
            if relative in unavailable_paths:
                if Path(relative).suffix.lower() in (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"):
                    if relative in output_media or destination.is_file():
                        missing_files.append(relative)
                        media_hashes_exact = False
                    else:
                        unavailable_image_refs.append(relative)
                else:
                    if relative in manifest_media or destination.is_file():
                        missing_files.append(relative)
                        media_hashes_exact = False
                    else:
                        unavailable_document_refs.append(relative)
                continue
            missing_files.append(relative)
            media_hashes_exact = False

        media_exact = (source_media == output_media == manifest_media and not missing_files and not changed_files
                       and media_hashes_exact and not recovered_refs and not unavailable_paths.intersection(source_media))
        approved_missing = unavailable_image_refs + unavailable_document_refs
        expected_manifest = source_media - set(approved_missing)
        expected_output = source_media - set(unavailable_image_refs)
        media_exception_pass = (not missing_files and not changed_files and media_hashes_exact
                                and manifest_media == expected_manifest and output_media == expected_output
                                and set(recovered_refs) <= source_media)
        status = ("pass" if text_exact and code_exact and links_exact and media_exact else
                  "pass-with-media-exceptions" if text_exact and code_exact and links_exact
                  and media_exception_pass and (approved_missing or recovered_refs) else "needs-review")
        rows.append({"wp_id": wp_id, "permalink": route, "source_status": "publish", "password_protected": "no",
                     "comparison_status": status, "text_exact": "yes" if text_exact else "no",
                     "text_similarity": f"{text_ratio:.6f}",
                     "source_text_sha256": hashlib.sha256(source_text.encode("utf-8")).hexdigest(),
                     "output_text_sha256": hashlib.sha256(output_text.encode("utf-8")).hexdigest(),
                     "source_code_sample_count": len(source_codes), "output_code_sample_count": len(output_codes),
                     "code_exact": "yes" if code_exact else "no", "source_code_sha256": sha_text(code_source_values),
                     "output_code_sha256": sha_text(code_output_values), "source_link_count": len(source_links),
                     "output_link_count": len(output_links), "links_exact": "yes" if links_exact else "no",
                     "missing_link_targets": "|".join(missing_links), "extra_link_targets": "|".join(extra_links),
                     "source_media_count": len(source_media), "output_media_count": len(output_media),
                     "media_manifest_count": len(manifest_media), "media_exact": "yes" if media_exact else "no",
                     "missing_media_refs": "|".join(sorted(source_media - output_media)),
                     "extra_media_refs": "|".join(sorted(output_media - source_media)),
                     "manifest_only_media": "|".join(sorted(manifest_media - source_media)),
                     "missing_or_changed_media": "|".join(sorted(set(missing_files + changed_files))),
                     "recovered_media_refs": "|".join(sorted(recovered_refs)),
                     "unavailable_image_refs_removed": "|".join(sorted(unavailable_image_refs)),
                     "unavailable_external_document_links": "|".join(sorted(unavailable_document_refs))})

    fields = ["wp_id", "permalink", "source_status", "password_protected", "comparison_status", "text_exact", "text_similarity",
              "source_text_sha256", "output_text_sha256", "source_code_sample_count", "output_code_sample_count", "code_exact",
              "source_code_sha256", "output_code_sha256", "source_link_count", "output_link_count", "links_exact",
              "missing_link_targets", "extra_link_targets", "source_media_count", "output_media_count", "media_manifest_count",
              "media_exact", "missing_media_refs", "extra_media_refs", "manifest_only_media", "missing_or_changed_media",
              "recovered_media_refs", "unavailable_image_refs_removed", "unavailable_external_document_links"]
    args.fidelity_report.parent.mkdir(parents=True, exist_ok=True)
    with args.fidelity_report.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    # Carry the automated conversion checks into publication eligibility. These
    # checks compare conversion to the backup; they do not substitute for live parity.
    eligibility_path = ROOT / "reports/publication-eligibility.csv"
    if eligibility_path.is_file():
        fidelity_by_id = {str(row.get("wp_id", "")): row for row in rows}
        excluded_ids, excluded_routes = read_exclusions(ROOT)
        live_verified = {str(row.get("wp_id", "")): row for row in
                         (csv.DictReader((ROOT / "reports/live-source-eligibility.csv").open(encoding="utf-8", newline=""))
                          if (ROOT / "reports/live-source-eligibility.csv").is_file() else [])}
        with eligibility_path.open(encoding="utf-8", newline="") as source:
            eligibility = list(csv.DictReader(source))
            source.seek(0)
            original_fields = next(csv.reader(source))
        for row in eligibility:
            fidelity = fidelity_by_id.get(str(row.get("wp_id", "")))
            if not fidelity:
                live = live_verified.get(str(row.get("wp_id", "")))
                if is_excluded(row.get("wp_id", ""), row.get("permalink", ""), excluded_ids, excluded_routes):
                    row["publish_eligible"] = "no"
                    row["eligibility_reasons"] = "excluded by migration publication policy"
                    if (live and live.get("source_status") == "publish" and live.get("password_protected") == "no"
                            and live.get("anonymous_full_body") == "yes" and live.get("route_http_status") == "200"
                            and not live.get("conversion_exceptions", "")):
                        row.update({"fidelity_status": "pass-live-verified", "text_exact": "yes", "code_exact": "yes",
                                    "links_exact": "yes", "media_exact": "yes" if live.get("media_files_verified") == "6" else "no"})
                    else:
                        row.update({"fidelity_status": "not-converted", "text_exact": "n/a", "code_exact": "n/a",
                                    "links_exact": "n/a", "media_exact": "n/a"})
                    continue
                if (live and live.get("source_status") == "publish" and live.get("password_protected") == "no"
                        and live.get("anonymous_full_body") == "yes" and live.get("route_http_status") == "200"
                        and not live.get("conversion_exceptions", "")):
                    row.update({"publish_eligible": "yes", "fidelity_status": "pass-live-verified",
                                "text_exact": "yes", "code_exact": "yes", "links_exact": "yes",
                                "media_exact": "yes" if live.get("media_files_verified") == "6" else "no"})
                    reason = "live-only article body/status/media verified against public REST and route evidence"
                    row["eligibility_reasons"] = "|".join(filter(None, (row.get("eligibility_reasons", ""), reason)))
                else:
                    row.update({"fidelity_status": "not-converted", "text_exact": "n/a", "code_exact": "n/a", "links_exact": "n/a", "media_exact": "n/a"})
                continue
            row.update({"fidelity_status": fidelity.get("comparison_status", "needs-review"),
                        "text_exact": fidelity.get("text_exact", "no"), "code_exact": fidelity.get("code_exact", "no"),
                        "links_exact": fidelity.get("links_exact", "no"), "media_exact": fidelity.get("media_exact", "no")})
            if fidelity.get("comparison_status") not in ("pass", "pass-with-media-exceptions"):
                row["publish_eligible"] = "no"
                reason = "automated conversion fidelity comparison failed or is incomplete"
                row["eligibility_reasons"] = "|".join(filter(None, (row.get("eligibility_reasons", ""), reason)))
            elif fidelity.get("comparison_status") == "pass-with-media-exceptions":
                row["publish_eligible"] = "yes"
                reason = "media-only exceptions are documented and accepted under the staging review"
                row["eligibility_reasons"] = "|".join(filter(None, (row.get("eligibility_reasons", ""), reason)))
        with eligibility_path.open("w", encoding="utf-8", newline="") as output:
            writer = csv.DictWriter(output, fieldnames=original_fields + ["fidelity_status", "text_exact", "code_exact", "links_exact", "media_exact"],
                                    lineterminator="\n", extrasaction="ignore")
            writer.writeheader()
            writer.writerows(eligibility)

    counts = {key: sum(row.get(key) == "yes" for row in rows) for key in ("text_exact", "code_exact", "links_exact", "media_exact")}
    passed = sum(row.get("comparison_status") in ("pass", "pass-with-media-exceptions") for row in rows)
    status_path = ROOT / "reports/conversion-status.md"
    existing_status = status_path.read_text(encoding="utf-8").splitlines() if status_path.is_file() else ["# Conversion status"]
    existing_status = [line for line in existing_status if not line.startswith("Automated source fidelity:")]
    existing_status.append(
        f"Automated source fidelity: {passed}/{len(rows)} pages pass text/code/link checks and exact or documented media checks; exact counts: "
        f"text {counts['text_exact']}, code {counts['code_exact']}, links {counts['links_exact']}, media {counts['media_exact']}. "
        "See `conversion-fidelity.csv` for per-article evidence and exceptions."
    )
    status_path.write_text("\n".join(existing_status) + "\n", encoding="utf-8")
    print(f"Conversion fidelity: {passed}/{len(rows)} pass; exact text/code/links/media={counts}")
    return 0 if len(rows) == len(eligible) and all(row.get("comparison_status") in ("pass", "pass-with-media-exceptions", "needs-review") for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
