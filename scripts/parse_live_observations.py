#!/usr/bin/env python3
"""Normalize public archive and sitemap observations from a saved live crawl."""
from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from discover_live import safe_name  # noqa: E402
from inventory import HomeCards  # noqa: E402

CRAWL = ROOT / "migration-review/live-crawl"
DIAGNOSTICS = ROOT / "reports/live-fetch-diagnostics.csv"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
BLOCKS = {"address", "article", "blockquote", "dd", "div", "dl", "dt", "figcaption", "h1", "h2", "h3", "h4", "h5", "h6", "li", "ol", "p", "pre", "section", "table", "tr", "ul"}
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def digest(value) -> str:
    encoded = json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def clean_text(value: str) -> str:
    value = unicodedata.normalize("NFC", html.unescape(value))
    return re.sub(r"\s+", " ", value).strip()


def clean_code(value: str) -> str:
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.rstrip() for line in value.splitlines()).strip("\n")


def clean_url(value: str) -> str:
    value = html.unescape(value.strip())
    if value.startswith("//"):
        value = "https:" + value
    parsed = urlparse(value)
    upload_marker = "/wp-content/uploads/"
    if upload_marker in parsed.path:
        relative = parsed.path.split(upload_marker, 1)[1]
        suffix = (("?" + parsed.query) if parsed.query else "") + (("#" + parsed.fragment) if parsed.fragment else "")
        return upload_marker + relative + suffix
    if parsed.hostname and parsed.hostname.lower() in ("networkstatic.net", "www.networkstatic.net"):
        return (parsed.path or "/") + (("?" + parsed.query) if parsed.query else "") + (("#" + parsed.fragment) if parsed.fragment else "")
    if parsed.hostname:
        host = parsed.hostname.lower().removeprefix("www.")
        return f"{parsed.scheme.lower()}://{host}{parsed.path}" + (("?" + parsed.query) if parsed.query else "") + (("#" + parsed.fragment) if parsed.fragment else "")
    return value


def parse_srcset(value: str) -> list[str]:
    result = []
    for candidate in value.split(","):
        parts = candidate.strip().split()
        if parts:
            result.append(clean_url(parts[0]))
    return result


class ArticlePage(HTMLParser):
    """Extract visible post/page structure without running page scripts."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.in_title = False
        self.published = ""
        self.modified = ""
        self.in_content = False
        self.content_stack: list[str] = []
        self.text: list[str] = []
        self.links: list[dict[str, str]] = []
        self.anchor: dict | None = None
        self.media: set[str] = set()
        self.featured: set[str] = set()
        self.raw_media: set[str] = set()
        self.pre_depth = 0
        self.pre_text: list[str] = []
        self.inline_code_depth = 0
        self.inline_code: list[str] = []
        self.code: list[str] = []
        self.crayon_active = False
        self.crayon_root_depth = 0
        self.crayon_line_active = False
        self.crayon_line: list[str] = []
        self.crayon_lines: list[str] = []
        self.password_form = False
        self.password_required = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()
        if tag in ("h1", "h2") and "entry-title" in classes:
            self.in_title = True
        if tag == "time" and attrs.get("datetime") and not self.published:
            self.published = attrs["datetime"]
        if tag == "meta" and attrs.get("property") in ("article:modified_time", "og:updated_time"):
            self.modified = attrs.get("content", self.modified)
        if "post-password-required" in classes:
            self.password_required = True
        if tag == "form" and "post-password-form" in classes:
            self.password_form = True

        if not self.in_content and tag == "div" and "entry-content" in classes:
            self.in_content = True
            self.content_stack = ["div"]
            return

        if not self.in_content:
            if tag == "img" and "wp-post-image" in classes:
                if attrs.get("src"):
                    self.featured.add(clean_url(attrs["src"]))
                self.featured.update(parse_srcset(attrs.get("srcset", "")))
            return

        if tag in BLOCKS:
            self.text.append("\n")
        if tag == "a":
            self.anchor = {"href": clean_url(attrs.get("href", "")), "text": []}
            if "/wp-content/uploads/" in attrs.get("href", ""):
                self.media.add(clean_url(attrs["href"]))
        if tag == "img":
            if attrs.get("src"):
                self.media.add(clean_url(attrs["src"]))
            self.media.update(parse_srcset(attrs.get("srcset", "")))
            if attrs.get("alt"):
                self.text.extend((" ", attrs["alt"], " "))
        if tag in ("iframe", "video", "audio", "source", "embed") and attrs.get("src"):
            self.media.add(clean_url(attrs["src"]))
        if tag == "div" and "crayon-syntax" in classes:
            self.crayon_active = True
            self.crayon_root_depth = len(self.content_stack) + 1
            self.crayon_lines = []
        if tag == "div" and "crayon-line" in classes:
            self.crayon_line_active = True
            self.crayon_line = []
        if tag == "pre":
            self.pre_depth += 1
            if self.pre_depth == 1:
                self.pre_text = []
        elif tag == "code" and self.pre_depth == 0:
            self.inline_code_depth += 1
            if self.inline_code_depth == 1:
                self.inline_code = []
        if tag not in VOID:
            self.content_stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in ("h1", "h2"):
            self.in_title = False
        if not self.in_content:
            return
        if tag == "a" and self.anchor is not None:
            text = clean_text("".join(self.anchor["text"]))
            if text or self.anchor["href"]:
                self.links.append({"text": text, "href": self.anchor["href"]})
            self.anchor = None
        if tag == "div" and self.crayon_line_active:
            line = clean_code("".join(self.crayon_line).replace("\xa0", " "))
            self.crayon_lines.append(line)
            self.crayon_line_active = False
            self.crayon_line = []
        if tag == "pre" and self.pre_depth:
            self.pre_depth -= 1
            if self.pre_depth == 0:
                self.code.append(clean_code("".join(self.pre_text)))
        elif tag == "code" and self.inline_code_depth and self.pre_depth == 0:
            self.inline_code_depth -= 1
            if self.inline_code_depth == 0:
                self.code.append(clean_code("".join(self.inline_code)))
        crayon_root_end = tag == "div" and self.crayon_active and len(self.content_stack) == self.crayon_root_depth
        if crayon_root_end:
            value = clean_code("\n".join(self.crayon_lines))
            if value:
                self.code.append(value)
            self.crayon_active = False
            self.crayon_root_depth = 0
        if tag in self.content_stack:
            index = len(self.content_stack) - 1 - self.content_stack[::-1].index(tag)
            self.content_stack = self.content_stack[:index]
            if not self.content_stack:
                self.in_content = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_content:
            if self.anchor is not None:
                self.anchor["text"].append(data)
            for match in re.findall(r"(?:https?:)?//[^\s\"'<>]*?/wp-content/uploads/[^\s\"'<>]+|/wp-content/uploads/[^\s\"'<>]+", data, re.I):
                self.raw_media.add(clean_url(match.rstrip(".,;")))
            if self.crayon_line_active:
                self.crayon_line.append(data)
            elif self.pre_depth:
                self.pre_text.append(data)
            elif self.inline_code_depth:
                self.inline_code.append(data)
            elif not self.crayon_active:
                self.text.append(data)

    def result(self) -> dict:
        text = clean_text("".join(self.text))
        links = sorted(set((x["text"], x["href"]) for x in self.links))
        code = [item for item in self.code if item]
        media = sorted(self.media)
        media = sorted(set(media) | self.raw_media)
        featured = sorted(self.featured)
        return {
            "title": clean_text(self.title), "published": self.published, "modified": self.modified,
            "body_text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest() if text else "",
            "body_text_chars": len(text), "code_block_count": len(code), "code_sha256": digest(code),
            "link_count": len(links), "links_sha256": digest(links),
            "link_records": json.dumps(links, ensure_ascii=False, separators=(",", ":")),
            "media_ref_count": len(media), "media_sha256": digest(media),
            "media_paths": json.dumps(media, ensure_ascii=False, separators=(",", ":")),
            "featured_media_paths": json.dumps(featured, ensure_ascii=False, separators=(",", ":")),
            "password_form_present": "yes" if self.password_form or self.password_required else "no",
        }


def load_diagnostics() -> dict[str, dict]:
    if not DIAGNOSTICS.is_file():
        return {}
    by_url = defaultdict(list)
    with DIAGNOSTICS.open(encoding="utf-8", newline="") as source:
        for row in csv.DictReader(source):
            by_url[row.get("requested_url", "")].append(row)
    result = {}
    for url, rows in by_url.items():
        good = [row for row in rows if row.get("http_status") and int(row["http_status"]) < 400]
        result[url] = (good or rows)[-1]
    return result


def page_metadata(url: str, diagnostics: dict[str, dict]) -> dict:
    row = diagnostics.get(url, {})
    saved = row.get("saved_file", "")
    path = ROOT / saved if saved else CRAWL / safe_name(url)
    parsed = ArticlePage()
    if path.is_file() and (row.get("http_status") == "200" or not row):
        try:
            parsed.feed(path.read_text(encoding="utf-8", errors="replace"))
        except (OSError, ValueError):
            pass
    values = parsed.result()
    return {
        **values,
        "fetch_http_status": row.get("http_status", ""),
        "fetch_result": row.get("result", "not-attempted"),
        "fetch_attempted_at_utc": row.get("attempted_at_utc", ""),
        "fetch_retrieval_method": row.get("retrieval_method", ""),
        "fetch_content_type": row.get("content_type", ""),
        "fetch_response_bytes": row.get("response_bytes", ""),
        "fetch_response_sha256": row.get("response_sha256", ""),
        "fetch_saved_file": saved,
    }


def main() -> int:
    diagnostics = load_diagnostics()
    archive_cards: dict[str, dict] = {}
    archive_rows: list[dict] = []
    for page in range(2, 24):
        url = f"https://networkstatic.net/page/{page}/"
        filename = CRAWL / f"page__{page}.html"
        if not filename.is_file():
            continue
        parser = HomeCards()
        parser.feed(filename.read_text(encoding="utf-8", errors="replace"))
        archive_response = diagnostics.get(url, {})
        for card in parser.items:
            parsed_url = urlparse(card["url"])
            path = parsed_url.path or "/"
            archive_cards[path] = {**card, "archive_page": page}
            article_url = "https://networkstatic.net" + path
            article_response = diagnostics.get(article_url, {})
            article_status = article_response.get("http_status", "")
            archive_rows.append({
                "url": card["url"], "path": path, "title": card["title"],
                "published": card.get("published", ""), "archive_page": page,
                "categories": card.get("categories", ""), "tags": card.get("tags", ""),
                "individual_article_status": (article_status or "not individually fetched"),
                "archive_http_status": archive_response.get("http_status", ""),
                "archive_retrieval_method": archive_response.get("retrieval_method", ""),
                "archive_fetched_at_utc": archive_response.get("attempted_at_utc", ""),
                "archive_response_sha256": archive_response.get("response_sha256", ""),
                "archive_saved_file": archive_response.get("saved_file", ""),
            })

    sitemap_rows: list[dict] = []
    content_urls: list[str] = []
    for kind in ("post", "page"):
        sitemap_path = CRAWL / f"{kind}-sitemap.xml.html"
        if not sitemap_path.is_file():
            continue
        root = ET.parse(sitemap_path).getroot()
        for item in root.findall("s:url", NS):
            loc = item.findtext("s:loc", namespaces=NS) or ""
            parsed = urlparse(loc)
            route = parsed.path or "/"
            if route == "/":
                continue
            lastmod = item.findtext("s:lastmod", default="", namespaces=NS)
            content_urls.append(loc)
            metadata = page_metadata(loc, diagnostics)
            card = archive_cards.get(route, {})
            sitemap_rows.append({
                "sitemap_type": kind, "url": loc, "path": route, "lastmod": lastmod,
                "listed_on_archive": "yes" if card else "no",
                "archive_page": card.get("archive_page", ""),
                "card_title": card.get("title", ""),
                "title": metadata["title"] or card.get("title", ""),
                "published": metadata["published"] or card.get("published", ""),
                **metadata,
            })

    write_csv(ROOT / "reports/live-archive-observations.csv", archive_rows,
              ["url", "path", "title", "published", "archive_page", "categories", "tags",
               "individual_article_status", "archive_http_status", "archive_retrieval_method",
               "archive_fetched_at_utc", "archive_response_sha256", "archive_saved_file"])
    write_csv(ROOT / "reports/live-sitemap-observations.csv", sitemap_rows,
              ["sitemap_type", "url", "path", "lastmod", "listed_on_archive", "archive_page",
               "card_title", "title", "published", "fetch_http_status", "fetch_result",
               "fetch_attempted_at_utc", "fetch_retrieval_method", "fetch_content_type",
               "fetch_response_bytes", "fetch_response_sha256", "fetch_saved_file",
               "body_text_sha256", "body_text_chars", "code_block_count", "code_sha256",
               "link_count", "links_sha256", "link_records", "media_ref_count", "media_sha256",
               "media_paths", "featured_media_paths", "password_form_present", "modified"])
    url_file = ROOT / "migration-review/live-content-urls.txt"
    url_file.parent.mkdir(parents=True, exist_ok=True)
    url_file.write_text("\n".join(dict.fromkeys(content_urls)) + "\n", encoding="utf-8")
    print(f"Archive cards: {len(archive_rows)} from {len({row['archive_page'] for row in archive_rows})} pages; "
          f"sitemap routes: {len(sitemap_rows)}; content URL list: {url_file.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
