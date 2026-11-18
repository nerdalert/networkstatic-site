# Migration exceptions and accepted differences

## Publication set

The machine-readable ledger approves all 191 migrated pages: 183 backup posts, 7 backup pages, and the verified April 17, 2023 live-only post. Every source is public and unprotected. The source audit confirms 55 nonpublic backup records excluded, zero published password-protected records, zero draft-only media copied, and no review output tracked in Git. Excluded counts are reported without draft titles or content.

## Live and backup differences

The live crawl covered all 191 publicly listed content routes with HTTP 200 responses. Anonymous REST responses confirm `publish` and `content.protected=false`. All 190 backup routes appear in the live sitemaps; no backup-only route is classified as deleted. Eighteen route/title differences and article-specific body/code/link/media differences are recorded in `live-vs-backup.csv` and `live-content-comparison.csv`. These differences were reviewed and accepted as nonblocking. The April post is separately verified in `content-verification.csv` and `live-source-eligibility.csv`.

Backup conversion checks pass for all 190 articles: visible text, code, and links match exactly. Media is exact for 187 articles. Three pages pass with documented media exceptions; details are in `conversion-fidelity.csv`.

## Link exceptions

Six broken local references were resolved:

- Four WordPress attachment-page links now point directly to their backed-up media files.
- The malformed Docker Machine route now resolves to `/normalizing-the-cloud-with-docker-machine/`.
- The historical OVS URL was externalized to its WordPress.com route. The current host returned HTTP 406 through the available retrieval method, so the result is inconclusive; the link remains external and does not block publication.

The target post ID 4867 linked from post ID 111 is included in the published set. Its current live route returned HTTP 404, but the preserved link resolves to the generated local article route. `reports/link-exceptions.csv` contains 21 additional per-link review entries; the final staging audit finds zero broken local references.

## Missing media

Recovery attempts covered all 17 media files absent from the supplied uploads tree. Fourteen Tech Field Day images were fetched and hashed. Three files remain unavailable: an empty vCider image anchor, the vCider Cassandra benchmark PDF, and the SDNCentral PDF. The empty anchor was removed with whitespace preserved; the two external PDF links remain in the articles with their surrounding explanatory text. See `missing-media-recovery.csv`, `missing-media-fetch-diagnostics.csv`, and `external-link-exceptions.csv` for per-file paths, attempts, statuses, hashes, and disposition.

## Staging validation

The local Pages build uses `https://nerdalert.github.io/networkstatic-site/`. Audit results: 519 HTML pages, 519 `noindex` pages, 184 articles, 7 migrated pages, 191 search records, 113 feeds, 1,179 RSS items, 1 sitemap, zero broken local references, and 307,640,676 output bytes. Repository, staged-file, Git-history, and generated-output scans report zero security findings. The report is `staging-local-audit.json`.

## Deployed staging verification

The audited source is public at [github.com/nerdalert/networkstatic-site](https://github.com/nerdalert/networkstatic-site), commit `efae69af9f4a8660d7c6b2ea58003cf51e8e1992`. GitHub Pages is configured for Actions and deployed successfully in [Actions run 44218270273](https://github.com/nerdalert/networkstatic-site/actions/runs/44218270273). The staging URL is [https://nerdalert.github.io/networkstatic-site/](https://nerdalert.github.io/networkstatic-site/).

Remote HTTP checks returned 200 for the home page, a representative article, search page and JavaScript, 191-record search index, RSS feed, sitemap, and profile photo. The home page and article carry `noindex`. Chrome rendering confirmed the home-page post list and sidebar, article text and media, and search page render correctly. The full local staging audit reports 519 HTML pages, all 519 noindex, 191 search records, 113 feeds, one sitemap, and zero broken local references. The repository/history and generated-output security scans passed with zero findings.

GitHub Pages has no custom domain configured. The generated staging site is about 308 MB, below the 1 GB Pages site limit. GitHub warned that one 53.18 MB MP3 exceeds its 50 MB recommendation; it remains below the enforced 100 MB individual-file limit. Production DNS, production custom-domain configuration, and the original WordPress site remain unchanged.
