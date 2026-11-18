# Migration exceptions and production verification

## Publication set

The publication ledger approves 190 backup sources: 183 posts and 7 pages. All have `post_status == publish`, no password, and passing automated conversion checks. Fifty-five nonpublic backup records are excluded; zero published password-protected records were found. A separately verified live-only route is excluded by `config/publication-exclusions.csv`; its page and six exclusive images are absent from the production output. Excluded nonpublic counts are reported without titles or content.

## Live and backup differences

The live crawl covered 191 publicly listed post/page routes with HTTP 200 responses. Anonymous REST responses confirm `publish` and `content.protected=false`. All 190 backup routes appear in the live sitemaps; no backup-only route is classified as deleted. Eighteen title differences and article-specific body/code/link/media differences are recorded in `live-vs-backup.csv` and `live-content-comparison.csv`. The user accepted these as nonblocking. These live-parity differences do not override the automated conversion checks.

Backup conversion checks pass for all 190 sources: visible text, code, and links match exactly. Media is exact for 187 sources; three pass with documented media-only exceptions in `conversion-fidelity.csv`.

## Link exceptions

Six broken local references were resolved: four attachment-page links now target their local media, the malformed Docker Machine route now points to its matching post, and the historical OVS link is preserved as an external WordPress route. The user-requested internal target with backup post ID 4867 is included in the eligible set, so its migrated link resolves locally even though the old live route returned HTTP 404. Twenty-one additional per-link review entries are documented in `link-exceptions.csv`.

The final full production audit found zero broken local references. Historically broken external links remain external and are listed in `external-link-exceptions.csv`; they do not block publication.

## Missing media

Recovery attempts covered all 17 files missing from the backup. Fourteen Tech Field Day images were fetched and hashed. Three files remain unavailable: an empty vCider image anchor, the vCider Cassandra benchmark PDF, and the SDNCentral PDF. The empty anchor was removed while preserving surrounding text; the two unavailable PDFs remain external links with explanatory text. Per-file attempts and dispositions are in `missing-media-recovery.csv`, `missing-media-fetch-diagnostics.csv`, and `external-link-exceptions.csv`.

## Production build and security audit

The production build uses `https://networkstatic.net/` and contains 514 HTML files, 183 article pages, 7 migrated pages, 190 search records, 111 RSS feeds with 1,169 items, and one sitemap. All HTML has production canonical URLs and no `noindex`; there are zero broken local references. The output is 306,397,024 bytes across 1,268 files. The full local route/output audit is in `production-local-audit.json`.

The GitHub Actions production workflow passed for commit `d853b67a7020af72309fcac9e884b4b0f0f67b7c` in [run 44227290680](https://github.com/nerdalert/networkstatic-site/actions/runs/44227290680). It built with Hugo 0.170.0 and pinned CleanWhite, then passed route, canonical/noindex, source eligibility, search/feed/sitemap, and repository/history/generated-output security checks. The security scan found zero findings.

## Live HTTP and browser verification

The deployed site at [https://networkstatic.net/](https://networkstatic.net/) serves the production root build. The homepage, archive, search, two representative articles, CSS, search JavaScript, 190-record search index, root RSS, sitemap, site mark, and profile image returned HTTP 200. The homepage and articles have root-domain canonical URLs, no `noindex` metadata, and no `/networkstatic-site/` references. The sitemap contains 302 root-domain URLs. The root RSS contains eligible content and no excluded route. The configured route exclusion and obsolete `/networkstatic-site/` URL both return 404 by design.

The search UI was exercised in Chrome: searching `OpenFlow` returned 30 matches, and result links use root-relative routes. Chrome screenshots of the live homepage at desktop and mobile widths and a representative article show the customized CleanWhite-inspired editorial layout: compact header, post list, user-requested profile sidebar, article typography, and code styling. The custom overrides shape the appearance, so the result is a NetworkStatic design built in the CleanWhite direction rather than an untouched upstream theme page. The CSS uses system font fallbacks and does not request external webfonts.

The apex DNS resolves to GitHub Pages; `www` redirects to the apex. GitHub Pages has an approved certificate and HTTPS enforcement enabled. Both `http://networkstatic.net/` and `http://www.networkstatic.net/` redirect to `https://networkstatic.net/`. The user reports DNS is correct and active; this migration made no DNS, MX, or mail-record changes.
