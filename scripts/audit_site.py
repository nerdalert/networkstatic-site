#!/usr/bin/env python3
"""Audit a rendered Hugo site for route, staging, and output-size failures."""
from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
import tomllib
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse


class PageRefs(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.refs: list[tuple[str, str]] = []
        self.robots: list[str] = []
        self.canonicals: list[str] = []
        self.og_urls: list[str] = []
        self.meta_urls: list[str] = []
        self.article_pages = 0
        self.migrated_pages = 0
        self.article_sections: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        a = dict(attrs)
        if tag == "article" and "article-page" in a.get("class", "").split():
            if a.get("data-section") == "posts":
                self.article_pages += 1
                self.article_sections.append("posts")
            elif a.get("data-section") == "pages":
                self.migrated_pages += 1
                self.article_sections.append("pages")
        if tag == "meta" and a.get("name", "").lower() == "robots":
            self.robots.append(a.get("content", "").lower())
        if tag == "meta" and a.get("property", "").lower() == "og:url":
            self.og_urls.append(a.get("content", ""))
        if tag == "meta" and a.get("content") and (a.get("property", "").lower().startswith("og:") or a.get("name", "").lower().startswith("twitter:")):
            self.meta_urls.append(a["content"])
        if tag == "link" and "canonical" in a.get("rel", "").lower().split():
            self.canonicals.append(a.get("href", ""))
            if a.get("href"):
                self.refs.append((a["href"], "canonical"))
        for name in ("href", "src", "poster", "data-src", "data-lazy-src", "data-original"):
            value = a.get(name)
            if value:
                self.refs.append((value.strip(), name))
        if a.get("srcset"):
            for part in a["srcset"].split(","):
                bits = part.strip().split()
                if bits:
                    self.refs.append((bits[0], "srcset"))
        if tag == "meta" and a.get("property", "").lower() in ("og:url", "og:image") and a.get("content"):
            self.refs.append((a["content"], "metadata"))


def output_target(site: Path, page: Path, raw: str, base: str) -> Path | None:
    raw = html.unescape(raw.strip())
    if not raw or raw.startswith(("#", "data:", "mailto:", "tel:", "javascript:", "blob:")):
        return None
    base_parts = urlparse(base)
    page_rel = page.relative_to(site).as_posix()
    page_url = urljoin(base, page_rel)
    resolved = urlparse(urljoin(page_url, raw))
    if resolved.scheme not in ("http", "https"):
        return None
    if resolved.netloc.lower() != base_parts.netloc.lower():
        return None
    base_path = base_parts.path or "/"
    if not base_path.endswith("/"):
        base_path += "/"
    path = unquote(resolved.path)
    if not path.startswith(base_path):
        raise ValueError(f"URL escapes Pages base path: {raw}")
    local = path[len(base_path):]
    if not local or local.endswith("/"):
        local += "index.html"
    target = (site / local).resolve()
    if not target.is_relative_to(site.resolve()):
        raise ValueError(f"URL resolves outside output directory: {raw}")
    if target.is_dir():
        target = target / "index.html"
    return target


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", type=Path, required=True)
    ap.add_argument("--mode", choices=("review", "staging", "production"), required=True)
    ap.add_argument("--base-url", required=True)
    ap.add_argument("--require-content", action="store_true")
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()
    site = args.site.resolve()
    if not site.is_dir():
        print(f"FAIL: output directory does not exist: {site}", file=sys.stderr)
        return 1
    base = args.base_url.rstrip("/") + "/"
    base_parts = urlparse(base)
    if base_parts.scheme not in ("http", "https") or not base_parts.netloc:
        print("FAIL: --base-url must be an absolute HTTP(S) URL", file=sys.stderr)
        return 1

    paths = list(site.rglob("*"))
    failures: list[str] = []
    for path in paths:
        if path.is_symlink():
            failures.append(f"symbolic link is not allowed in Pages output: {path.relative_to(site)}")
    files = [p for p in paths if p.is_file() and not p.is_symlink()]
    html_files = [p for p in files if p.suffix.lower() in (".html", ".htm")]
    total_bytes = sum(p.stat().st_size for p in files)
    broken: list[tuple[Path, str]] = []
    article_pages = 0
    migrated_pages = 0
    article_routes: set[str] = set()
    noindex_pages = 0
    search_count = 0
    feed_count = 0
    feed_item_count = 0
    sitemap_count = 0
    source_route_by_output: dict[str, str] = {}
    placeholder = re.compile(r"lorem ipsum|under construction|article archive is being prepared|replace this text", re.I)
    raw_shortcode = re.compile(r"\[/?(?:fancy_header3|image_frame|crayon|fancy_list|fancy_numbers|fancy_link|download_link|pullquote[1-4]|titled_box|colored_box|info_box|note_box|warning_box|slideshare|gview)\b", re.I)
    for page in html_files:
        text = page.read_text(encoding="utf-8", errors="replace")
        parser = PageRefs()
        parser.feed(text)
        article_pages += parser.article_pages
        migrated_pages += parser.migrated_pages
        if parser.robots and all("noindex" in value for value in parser.robots):
            noindex_pages += 1
        if parser.article_sections:
            relative = page.relative_to(site).parent.as_posix()
            article_routes.add("/" if relative == "." else "/" + relative.strip("/") + "/")
        if args.mode in ("review", "staging"):
            if not parser.robots or any("noindex" not in value for value in parser.robots):
                failures.append(f"staging HTML missing noindex metadata: {page.relative_to(site)}")
            if parser.canonicals:
                failures.append(f"staging HTML must not publish canonical tags: {page.relative_to(site)}")
            for u in parser.og_urls:
                if "networkstatic.net" in u.lower():
                    failures.append(f"staging og:url points at production: {page.relative_to(site)}")
            if any("networkstatic.net" in u.lower() for u in parser.meta_urls):
                failures.append(f"staging metadata points at production: {page.relative_to(site)}")
            if any("networkstatic.net" in raw.lower() for raw, _ in parser.refs):
                failures.append(f"staging local link/media points at production: {page.relative_to(site)}")
        else:
            if not parser.canonicals or any(not u.startswith("https://networkstatic.net/") for u in parser.canonicals):
                failures.append(f"production HTML has missing or incorrect canonical URL: {page.relative_to(site)}")
            if any("noindex" in value for value in parser.robots):
                failures.append(f"production HTML is marked noindex: {page.relative_to(site)}")
        if placeholder.search(text):
            failures.append(f"visible placeholder text found: {page.relative_to(site)}")
        # Shortcode examples in code blocks are legitimate historical content.
        outside_code = re.sub(r"<(pre|code)\b[^>]*>.*?</\1\s*>", "", text, flags=re.I | re.S)
        if raw_shortcode.search(outside_code) or "{{< relurl" in outside_code:
            failures.append(f"unconverted shortcode syntax found: {page.relative_to(site)}")
        for raw, _kind in parser.refs:
            if args.mode == "production":
                target_url = urlparse(raw)
                if target_url.path.startswith("/networkstatic-site/") or (
                        target_url.netloc.lower() == "networkstatic.net"
                        and target_url.path.startswith("/networkstatic-site/")):
                    failures.append(f"production link retains the obsolete project subpath: {page.relative_to(site)}")
            try:
                target = output_target(site, page, raw, base)
            except ValueError as exc:
                failures.append(f"{page.relative_to(site)}: {exc}")
                continue
            if target is not None and not target.is_file():
                broken.append((page.relative_to(site), raw))

    if args.require_content and article_pages == 0:
        failures.append("no migrated article pages are present; refusing empty/placeholder staging")
    approved_routes: set[str] = set()
    approved_ids: set[str] = set()
    if args.mode in ("staging", "production"):
        repo = Path(__file__).resolve().parents[1]
        ledger_path = repo / "reports/publication-eligibility.csv"
        source_audit_path = repo / "reports/migration-source-audit.json"
        try:
            with ledger_path.open(encoding="utf-8", newline="") as handle:
                ledger_rows = list(csv.DictReader(handle))
            for row in ledger_rows:
                if row.get("publish_eligible") != "yes":
                    continue
                if row.get("source_status") != "publish" or row.get("source_password_protected") != "no":
                    failures.append("publication ledger approves a source without published/unprotected provenance")
                    continue
                route_path = urlparse(row.get("permalink", "")).path
                approved_routes.add("/" if not route_path.strip("/") else "/" + route_path.strip("/") + "/")
                if row.get("wp_id"):
                    approved_ids.add(str(row["wp_id"]))
            source_audit = json.loads(source_audit_path.read_text(encoding="utf-8"))
            source_by_id = {str(row.get("wp_id")): row for row in source_audit.get("migrated_sources", [])}
            if not source_audit.get("audit_passed"):
                failures.append("published-source audit did not pass for the production/staging source set")
        except (OSError, csv.Error, json.JSONDecodeError):
            failures.append("publication eligibility/source-provenance ledgers are missing or invalid")
            source_by_id = {}

        # Production content may contain WordPress rows only when the source
        # audit and the article-level allowlist both approve them.
        production_ids: set[str] = set()
        for content_file in (repo / "content").rglob("*.md"):
            source_text = content_file.read_text(encoding="utf-8", errors="replace")
            if not source_text.startswith("+++\n"):
                continue
            closing = source_text.find("\n+++\n", 4)
            if closing < 0:
                failures.append("production content has invalid TOML front matter")
                continue
            try:
                front = tomllib.loads(source_text[4:closing])
            except tomllib.TOMLDecodeError:
                failures.append("production content has unreadable TOML front matter")
                continue
            if front.get("wp_id") is None:
                continue
            wp_id = str(front.get("wp_id"))
            production_ids.add(wp_id)
            source = source_by_id.get(wp_id)
            if not source or source.get("post_status") != "publish" or source.get("password_protected") is not False:
                failures.append("production content contains a source without published/unprotected audit evidence")
            if (wp_id not in approved_ids or front.get("draft") is True or front.get("review_only") is True
                    or front.get("source_status") != "publish" or front.get("source_password_protected") is not False):
                failures.append("production content contains an unapproved or draft WordPress source")
            if source and front.get("source_content_sha256") != source.get("source_content_sha256"):
                failures.append("production content source hash differs from its verified provenance")
        if production_ids != approved_ids:
            failures.append("production WordPress files do not match the publication-eligible ID allowlist")
        if article_routes != approved_routes:
            failures.append("rendered article routes do not match the publication-eligible route allowlist")

        # The search index is an exact content allowlist, so review-only and
        # excluded posts cannot appear in deployed search results.
        try:
            search_index = json.loads((site / "search-index.json").read_text(encoding="utf-8"))
            search_count = len(search_index)
            base_path = base_parts.path or "/"
            if not base_path.endswith("/"):
                base_path += "/"
            search_routes: set[str] = set()
            for record in search_index:
                if not isinstance(record, dict) or not record.get("url"):
                    failures.append("deployed search index contains an invalid record")
                    continue
                target = urlparse(urljoin(base, record["url"]))
                if target.netloc.lower() != base_parts.netloc.lower() or not target.path.startswith(base_path):
                    failures.append("deployed search index includes a URL outside the Pages base path")
                    continue
                relative = unquote(target.path[len(base_path):])
                search_routes.add("/" if not relative.strip("/") else "/" + relative.strip("/") + "/")
            if search_routes != approved_routes or len(search_index) != len(search_routes):
                failures.append("deployed search index does not exactly match publication-eligible routes")
        except (OSError, json.JSONDecodeError, TypeError):
            failures.append("deployed search index is missing or invalid")

        # Validate feed and sitemap URLs as well as their membership. Article
        # records must stay within the same publication allowlist.
        base_path = base_parts.path or "/"
        if not base_path.endswith("/"):
            base_path += "/"
        for xml_file in files:
            if xml_file.suffix.lower() != ".xml":
                continue
            try:
                document = ET.parse(xml_file).getroot()
            except (ET.ParseError, OSError):
                failures.append("generated XML feed/sitemap is invalid")
                continue
            if document.tag.lower().endswith("rss"):
                feed_count += 1
                for item in document.findall(".//item"):
                    feed_item_count += 1
                    target = urlparse(urljoin(base, item.findtext("link", "")))
                    if target.netloc.lower() != base_parts.netloc.lower() or not target.path.startswith(base_path):
                        failures.append("deployed RSS item points outside the Pages base path")
                        continue
                    relative = unquote(target.path[len(base_path):])
                    route = "/" if not relative.strip("/") else "/" + relative.strip("/") + "/"
                    local = site / (relative.strip("/") + "/index.html" if relative.strip("/") else "index.html")
                    if not local.is_file():
                        failures.append("deployed RSS item points to a missing local page")
                    if route in article_routes and route not in approved_routes:
                        failures.append("deployed RSS contains an article outside the publication allowlist")
            elif document.tag.lower().endswith("urlset"):
                sitemap_count += 1
                namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
                sitemap_routes: set[str] = set()
                for item in document.findall("s:url", namespace):
                    target = urlparse(urljoin(base, item.findtext("s:loc", "", namespace)))
                    if target.netloc.lower() != base_parts.netloc.lower() or not target.path.startswith(base_path):
                        failures.append("deployed sitemap includes a URL outside the Pages base path")
                        continue
                    relative = unquote(target.path[len(base_path):])
                    route = "/" if not relative.strip("/") else "/" + relative.strip("/") + "/"
                    sitemap_routes.add(route)
                    local = site / (relative.strip("/") + "/index.html" if relative.strip("/") else "index.html")
                    if not local.is_file():
                        failures.append("deployed sitemap points to a missing local page")
                if not approved_routes.issubset(sitemap_routes):
                    failures.append("deployed sitemap omits publication-eligible article routes")
        if sitemap_count == 0:
            failures.append("deployed sitemap output is missing or invalid")
    if args.mode == "review":
        audit_path = Path(__file__).resolve().parents[1] / "reports/migration-source-audit.json"
        try:
            source_audit = json.loads(audit_path.read_text(encoding="utf-8"))
            source_rows = source_audit.get("migrated_sources", [])
            expected_posts = sum(row.get("post_type") == "post" for row in source_rows)
            expected_pages = sum(row.get("post_type") == "page" for row in source_rows)
            if not source_audit.get("audit_passed"):
                failures.append("source eligibility audit did not pass before review build")
            if article_pages != expected_posts:
                failures.append(f"review article count mismatch: expected {expected_posts}, rendered {article_pages}")
            if migrated_pages != expected_pages:
                failures.append(f"review page count mismatch: expected {expected_pages}, rendered {migrated_pages}")
            expected_urls: set[str] = set()
            for row in source_rows:
                if row.get("post_status") != "publish" or row.get("password_protected") is not False:
                    failures.append("review source ledger contains a nonpublic or protected source")
                    continue
                content_path = Path(__file__).resolve().parents[1] / row["review_content_path"]
                try:
                    source = content_path.read_text(encoding="utf-8")
                    front_matter = source.split("+++", 2)[1]
                    source_url = tomllib.loads(front_matter).get("url")
                    if not source_url:
                        failures.append(f"review source has no explicit URL: {content_path.name}")
                    else:
                        expected_urls.add(source_url)
                        output_path = Path(source_url.strip("/")) / "index.html"
                        source_route_by_output[output_path.as_posix()] = source_url
                except (OSError, IndexError, tomllib.TOMLDecodeError):
                    failures.append(f"review source metadata could not be read: {content_path.name}")
        except (OSError, json.JSONDecodeError):
            failures.append("source eligibility audit is missing or invalid for review build")
            source_rows = []
            expected_urls = set()
        exception_path = Path(__file__).resolve().parents[1] / "reports/link-exceptions.csv"
        try:
            with exception_path.open(encoding="utf-8", newline="") as handle:
                exception_keys = {(row.get("source_permalink", ""), row.get("target_path", ""))
                                  for row in csv.DictReader(handle)}
            for page, raw in broken:
                source_route = source_route_by_output.get(page.as_posix())
                if not source_route:
                    continue
                target_path = unquote(urlparse(raw).path or raw)
                if (source_route, target_path) not in exception_keys:
                    failures.append(f"article link exception missing from publication ledger: {source_route} -> {target_path}")
        except OSError:
            failures.append("publication link-exception ledger is missing or unreadable")
        search_index_path = site / "search-index.json"
        try:
            search_index = json.loads(search_index_path.read_text(encoding="utf-8"))
            search_count = len(search_index)
            actual_urls = {record.get("url") for record in search_index if isinstance(record, dict)}
            if len(actual_urls) != len(search_index) or actual_urls != expected_urls:
                failures.append("review search index does not match the public, unprotected source URL allowlist")
        except (OSError, json.JSONDecodeError, TypeError):
            failures.append("review search index is missing or invalid")
        forbidden_outputs = {"index.xml", "sitemap.xml", "sitemap_index.xml"}
        present = sorted(path.relative_to(site).as_posix() for path in files if path.name in forbidden_outputs)
        if present:
            failures.append("review output unexpectedly includes a feed or sitemap: " + ", ".join(present))
    if total_bytes > 1_000_000_000:
        failures.append(f"published output exceeds the 1 GB GitHub Pages site limit ({total_bytes} bytes)")
    if (site / "CNAME").exists():
        failures.append("CNAME must not be present in staging or preview source output")
    for p in paths:
        rel = p.relative_to(site)
        if any(part.startswith(".") for part in rel.parts) and rel.as_posix() != ".nojekyll":
            failures.append(f"hidden output file/directory found: {rel}")
    failures.extend(f"broken local reference from {page}: {raw}" for page, raw in broken)

    largest = sorted(((p.stat().st_size, p.relative_to(site).as_posix()) for p in files), reverse=True)[:10]
    report = {"mode": args.mode, "base_url": base, "html_pages": len(html_files),
              "article_pages": article_pages, "migrated_pages": migrated_pages,
              "noindex_html_pages": noindex_pages,
              "approved_article_routes": sorted(approved_routes),
              "rendered_article_routes": sorted(article_routes),
              "search_index_records": search_count, "rss_feed_count": feed_count,
              "rss_item_count": feed_item_count, "sitemap_count": sitemap_count,
              "file_count": len(files), "output_bytes": total_bytes,
              "largest_files": [{"path": p, "bytes": n} for n, p in largest],
              "broken_local_references": len(broken),
              "broken_local_reference_details": [{"page": str(page), "url": raw} for page, raw in broken],
              "failures": failures}
    content_exceptions = []
    if args.mode == "review":
        content_exceptions = [failure for failure in failures
                              if failure.startswith(("unconverted shortcode syntax found:", "broken local reference from "))]
    blocking_failures = [failure for failure in failures if failure not in content_exceptions]
    report["content_exceptions"] = content_exceptions
    report["blocking_failures"] = blocking_failures
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    summary = {key: report[key] for key in ("mode", "base_url", "html_pages", "article_pages", "migrated_pages",
                                            "noindex_html_pages", "search_index_records", "rss_feed_count",
                                            "rss_item_count", "sitemap_count", "file_count", "output_bytes",
                                            "broken_local_references")}
    summary["failure_count"] = len(failures)
    summary["blocking_failure_count"] = len(blocking_failures)
    summary["content_exception_count"] = len(content_exceptions)
    summary["content_exception_samples"] = content_exceptions[:20]
    summary["additional_content_exceptions"] = max(0, len(content_exceptions) - 20)
    summary["blocking_failures"] = blocking_failures[:40]
    summary["additional_blocking_failures"] = max(0, len(blocking_failures) - 40)
    print(json.dumps(summary, indent=2))
    return 1 if blocking_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
