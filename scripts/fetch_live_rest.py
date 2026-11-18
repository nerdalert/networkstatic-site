#!/usr/bin/env python3
"""Fetch anonymous WordPress REST representations for every discovered live route."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def slug_from_path(path: str) -> str:
    return path.strip("/").split("/")[-1] if path.strip("/") else ""


def safe_slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", value)[:100] or "route"


def normalized_path(value: str) -> str:
    path = urlparse(value).path or "/"
    return "/" + path.strip("/") + "/" if path.strip("/") else "/"


def fetch(url: str, timeout: float) -> tuple[bytes, int, str, str]:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != "networkstatic.net":
        raise RuntimeError("request outside the networkstatic.net host was blocked")
    request = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
    })
    with urlopen(request, timeout=timeout) as response:
        body = response.read(20_000_001)
        if len(body) > 20_000_000:
            raise RuntimeError("response exceeded the 20 MB safety limit")
        return body, response.status, response.headers.get("Content-Type", ""), response.geturl()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, default=ROOT / "reports/live-sitemap-observations.csv")
    ap.add_argument("--output", type=Path, default=ROOT / "reports/live-rest-observations.csv")
    ap.add_argument("--save-dir", type=Path, default=ROOT / "migration-review/live-rest")
    ap.add_argument("--delay", type=float, default=0.2)
    ap.add_argument("--retries", type=int, default=2)
    ap.add_argument("--timeout", type=float, default=20)
    args = ap.parse_args()
    save_dir = args.save_dir.resolve()
    if not save_dir.is_relative_to((ROOT / "migration-review").resolve()):
        ap.error("--save-dir must stay inside ignored migration-review/")
    if args.delay < 0 or args.retries < 0:
        ap.error("delay and retry count must be nonnegative")

    input_rows = read_rows(args.input)
    diagnostics: list[dict[str, str]] = []
    successful = 0
    for index, source in enumerate(input_rows):
        path = normalized_path(source.get("path") or source.get("url", ""))
        kind = source.get("sitemap_type", "post")
        if kind not in ("post", "page"):
            diagnostics.append({"route": path, "sitemap_type": kind, "result": "unsupported-route-kind"})
            continue
        slug = slug_from_path(path)
        endpoint = f"https://networkstatic.net/wp-json/wp/v2/{'posts' if kind == 'post' else 'pages'}?"
        query = urlencode({"slug": slug, "_fields": "id,type,status,slug,link,date,date_gmt,modified,modified_gmt,title,content,excerpt,featured_media,categories,tags"})
        url = endpoint + query
        entry: dict[str, str] = {"route": path, "sitemap_type": kind, "slug": slug,
                                 "requested_url": url, "retrieval_method": "anonymous WordPress REST GET",
                                 "attempts": "", "result": "", "http_status": "", "api_row_count": "",
                                 "wp_id": "", "type": "", "source_status": "", "password_protected": "",
                                 "api_route": "", "title": "", "published": "", "modified": "",
                                 "content_bytes": "", "content_sha256": "", "response_bytes": "",
                                 "response_sha256": "", "saved_file": "", "transport_error": ""}
        last_error = ""
        for attempt in range(1, args.retries + 2):
            entry["attempts"] = str(attempt)
            try:
                body, status, content_type, final_url = fetch(url, args.timeout)
                entry.update({"http_status": str(status), "response_bytes": str(len(body)),
                              "response_sha256": hashlib.sha256(body).hexdigest()})
                if status != 200 or "json" not in content_type.lower():
                    entry["result"] = "unexpected-http-response"
                    last_error = f"HTTP {status}; content-type={content_type}"
                else:
                    result = json.loads(body)
                    if not isinstance(result, list):
                        raise ValueError("REST response was not a JSON array")
                    matches = [item for item in result if normalized_path(item.get("link", "")) == path]
                    entry["api_row_count"] = str(len(result))
                    if len(matches) != 1:
                        entry["result"] = "route-not-uniquely-matched"
                        last_error = f"REST slug query returned {len(result)} rows and {len(matches)} exact route matches"
                    else:
                        item = matches[0]
                        content = item.get("content", {})
                        output = save_dir / kind / (safe_slug(slug) + "-" + str(item.get("id", "")) + ".json")
                        output.parent.mkdir(parents=True, exist_ok=True)
                        output.write_bytes(body)
                        entry.update({"result": "matched", "final_url": final_url, "wp_id": str(item.get("id", "")),
                                      "type": item.get("type", ""), "source_status": item.get("status", ""),
                                      "password_protected": str(bool(content.get("protected", True))).lower(),
                                      "api_route": normalized_path(item.get("link", "")),
                                      "title": item.get("title", {}).get("rendered", ""),
                                      "published": item.get("date_gmt", ""), "modified": item.get("modified_gmt", ""),
                                      "content_bytes": str(len(content.get("rendered", "").encode("utf-8"))),
                                      "content_sha256": hashlib.sha256(content.get("rendered", "").encode("utf-8")).hexdigest(),
                                      "saved_file": output.relative_to(ROOT).as_posix()})
                        successful += 1
                        break
            except HTTPError as error:
                entry["http_status"] = str(error.code)
                last_error = f"HTTP {error.code} {error.reason}"
            except (URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError, RuntimeError) as error:
                last_error = f"{type(error).__name__}: {error}"
            if attempt <= args.retries and (not entry["http_status"] or entry["http_status"] in ("408", "429", "500", "502", "503", "504")):
                time.sleep(min(2**(attempt - 1), 4))
            else:
                break
        if entry["result"] != "matched":
            entry["transport_error"] = last_error
            entry["result"] = entry["result"] or "transport-error"
        diagnostics.append(entry)
        if args.delay and index < len(input_rows) - 1:
            time.sleep(args.delay)

    fields = ["route", "sitemap_type", "slug", "requested_url", "retrieval_method", "attempts", "result",
              "http_status", "final_url", "api_row_count", "wp_id", "type", "source_status", "password_protected",
              "api_route", "title", "published", "modified", "content_bytes", "content_sha256",
              "response_bytes", "response_sha256", "saved_file", "transport_error"]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(diagnostics)
    print(f"REST route retrieval: {successful}/{len(input_rows)} exact public routes; diagnostics={args.output}")
    return 0 if successful == len(input_rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
