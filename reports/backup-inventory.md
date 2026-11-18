# Initial migration inventory

- Backup logical source: `bbsali0_wrdp1.sql` (15,646,312 bytes; SHA-256 recorded in `inventory-summary.json`).
- Eligible backup content under the strict source gate: 183 unprotected published posts, 7 unprotected published pages; 1117 attachment records. Excluded counts by status/type are in `source-eligibility.json`; it contains no excluded titles or content.
- Upload candidates: 4,674 files (1,301,877,152 bytes). Literal-path scan finds 399 candidates; deterministic conversion has copied 568 dependencies (295,379,256 bytes) into the ignored local review tree, outside production roots. See `media-copy-manifest.csv` and `conversion-fidelity.csv` for dependency/hash checks.
- Live route inventory: 191 unique public post/page routes, including 8 supplied homepage cards, 175 archive cards across pages 2–23, 184 post-sitemap routes, and 7 page-sitemap routes. Direct response counts are `{'200': 191}`.
- Reconciliation: 183 backup posts and 7 backup pages have direct route observations (172 route/title matches and 18 title differences); 1 live-only route has no backup row. 0 backup posts and 0 backup pages remain unobserved candidates. Absence does not prove deletion.
- Local fetch diagnostics recorded 223 GET attempts across 223 requested URLs; result counts and transport errors are in `live-fetch-diagnostics.csv`. Requests use standard browser headers because the origin's ModSecurity returned 406 for the earlier descriptive crawler User-Agent. Browser-tool probes remain separate in `live-browser-probes.csv` and do not override direct HTTP evidence.
- The April 17, 2023 “ChatGPT your Project Docs” route is present in the public post sitemap and returns HTTP 200. Its WordPress REST record and media are in the ignored live crawl; full verification and conversion status are tracked separately in `content-verification.csv` and `live-content-comparison.csv`.

## Archive safety inspection

`inventory-summary.json` records archive size/hash, 16,600 members, path/link checks, duplicate paths, largest member, and oversized members. No paths escaped the archive root, no unsafe link targets were found, and no special files were present. Three in-archive symlinks and one repeated archive path were found. The backup was already present as an extracted directory; this workflow does not extract the tar or execute PHP.
