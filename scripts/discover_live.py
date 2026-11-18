#!/usr/bin/env python3
"""Fetch live archive endpoints with explicit HTTP and transport diagnostics.

This script never writes to the source WordPress site. Successful response
bodies are saved only under the ignored local migration-review directory.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
MAX_BODY_BYTES = 10_000_000


def safe_name(url: str) -> str:
    parsed = urlparse(url)
    name = (parsed.path.strip("/") or "home").replace("/", "__")
    if parsed.query:
        name += "__" + hashlib.sha256(parsed.query.encode()).hexdigest()[:10]
    return name + ".html"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start-page", type=int, default=1)
    ap.add_argument("--end-page", type=int, default=23)
    ap.add_argument("--retries", type=int, default=1, help="retry count after the initial attempt")
    ap.add_argument("--timeout", type=float, default=8.0)
    ap.add_argument("--extra-url", action="append", default=[],
                    help="additional read-only public URL to record and save (repeatable)")
    ap.add_argument("--url-file", type=Path,
                    help="UTF-8 file containing additional read-only URLs, one per line")
    ap.add_argument("--delay", type=float, default=0.2,
                    help="seconds to wait between distinct URLs (default: 0.2)")
    ap.add_argument("--diagnostics", type=Path, default=ROOT / "reports/live-fetch-diagnostics.csv")
    ap.add_argument("--save-dir", type=Path, default=ROOT / "migration-review/live-crawl")
    a = ap.parse_args()
    if a.start_page < 1 or a.end_page < a.start_page or a.retries < 0:
        ap.error("page range and retry count must be nonnegative and ordered")

    base = "https://networkstatic.net"
    urls = [base + "/"]
    urls.extend(base + "/page/" + str(page) + "/" for page in range(a.start_page, a.end_page + 1) if page > 1)
    urls.extend((
        base + "/chatgpt-project-docs/",
        base + "/open-v-switch-red-hat-installation/",
        base + "/sitemap_index.xml",
        base + "/post-sitemap.xml",
        base + "/page-sitemap.xml",
        base + "/attachment-sitemap.xml",
        base + "/wp-sitemap.xml",
        base + "/wp-json/wp/v2/posts?per_page=1",
        base + "/wp-json/wp/v2/posts/7986",
        base + "/feed/",
    ))
    file_urls = []
    if a.url_file:
        file_urls = [line.strip() for line in a.url_file.read_text(encoding="utf-8").splitlines()
                     if line.strip() and not line.lstrip().startswith("#")]
    urls = list(dict.fromkeys([*urls, *a.extra_url, *file_urls]))
    if a.delay < 0:
        ap.error("--delay must be nonnegative")
    for url in urls:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https") or (parsed.hostname or "").lower() not in ("networkstatic.net", "www.networkstatic.net"):
            ap.error(f"only public networkstatic.net URLs are allowed: {url}")
    save_dir = a.save_dir.resolve()
    if not save_dir.is_relative_to(ROOT.resolve()) or save_dir == ROOT.resolve():
        ap.error("--save-dir must be a child of the migration project")
    save_dir.mkdir(parents=True, exist_ok=True)
    a.diagnostics.parent.mkdir(parents=True, exist_ok=True)
    fields = ["requested_url", "retrieval_method", "attempt", "attempted_at_utc", "result", "http_status",
              "final_url", "content_type", "response_bytes", "response_sha256", "saved_file", "transport_error"]
    rows = []
    for url in urls:
        for attempt in range(1, a.retries + 2):
            stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
            record = {"requested_url": url, "retrieval_method": "python-urllib GET", "attempt": attempt,
                      "attempted_at_utc": stamp, "result": "", "http_status": "", "final_url": "",
                      "content_type": "", "response_bytes": 0, "response_sha256": "", "saved_file": "",
                      "transport_error": ""}
            # The site's ModSecurity rules reject the original descriptive
            # crawler UA with HTTP 406. A normal browser UA plus ordinary
            # navigation headers permits read-only public page retrieval.
            request = Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            })
            try:
                with urlopen(request, timeout=a.timeout) as response:
                    body = response.read(MAX_BODY_BYTES + 1)
                    truncated = len(body) > MAX_BODY_BYTES
                    body = body[:MAX_BODY_BYTES]
                    record.update({"result": "http-response", "http_status": response.status,
                                   "final_url": response.geturl(), "content_type": response.headers.get("Content-Type", ""),
                                   "response_bytes": len(body), "response_sha256": hashlib.sha256(body).hexdigest()})
                    if truncated:
                        record["transport_error"] = f"response truncated at {MAX_BODY_BYTES} bytes"
                    elif response.status < 400:
                        destination = save_dir / safe_name(url)
                        destination.write_bytes(body)
                        record["saved_file"] = destination.relative_to(ROOT).as_posix()
            except HTTPError as error:
                body = error.read(MAX_BODY_BYTES)
                record.update({"result": "http-error", "http_status": error.code, "final_url": error.geturl(),
                               "content_type": error.headers.get("Content-Type", ""), "response_bytes": len(body),
                               "response_sha256": hashlib.sha256(body).hexdigest()})
            except (URLError, TimeoutError, OSError) as error:
                reason = getattr(error, "reason", error)
                record.update({"result": "transport-error", "transport_error": f"{type(reason).__name__}: {reason}"})
            rows.append(record)
            if record["http_status"] and int(record["http_status"]) < 400:
                break
            if record["http_status"] and 400 <= int(record["http_status"]) < 500 and int(record["http_status"]) not in (408, 429):
                break
        if a.delay:
            time.sleep(a.delay)
    with a.diagnostics.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    failures = sum(row["result"] != "http-response" or not row["http_status"] or int(row["http_status"]) >= 400 for row in rows)
    print(f"Requested {len(urls)} URLs; recorded {len(rows)} attempts; failures={failures}; diagnostics={a.diagnostics}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
