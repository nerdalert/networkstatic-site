# NetworkStatic migration

This repository contains the Hugo migration of NetworkStatic, using CleanWhite pinned at `c4c7f2171e4c8244a8588fd6a101c48154ae1229` and Hugo 0.170.0. The original WordPress backup remains outside the repository and unchanged. Production DNS and the old WordPress site are untouched.

## Migration status

- The backup contains 183 published, unprotected posts and 7 published, unprotected pages. Fifty-five nonpublic records are excluded; no published password-protected records were found. Reports contain excluded counts only, not draft titles or content.
- The published source set contains 191 pages: all 190 backup routes plus the verified live-only April 17, 2023 “ChatGPT your Project Docs” article. The anonymous REST status, password flag, full body, links and six image assets were checked.
- Automated backup conversion checks pass for all 190 backup articles: text, code and links match exactly; media is exact for 187. The other three articles have documented media-only exceptions. All 14 recoverable Tech Field Day images were copied and hashed; three unavailable files were documented, and broken image/empty-anchor content was removed while preserving surrounding text. Two unavailable PDF links remain external.
- Eighteen live title differences and other accepted live-body differences are recorded in `reports/live-content-comparison.csv` and `reports/live-vs-backup.csv`; they do not block the approved published content set.
- The staging build passes on `https://nerdalert.github.io/networkstatic-site/`: all 519 HTML pages are `noindex`, all 191 migrated routes are present in search, feeds and sitemap, there are zero broken local references, and output size is about 308 MB. Repository, staged files, Git history and generated output scans report no findings.
- All 191 public, unprotected pages are approved by `reports/publication-eligibility.csv`. The production `content/` and `static/` trees contain only the approved pages and their owned media. Drafts, private/protected records, other nonpublic records, and their exclusive media are excluded.
- GitHub Pages staging deployment is the next step. The repository URL is `https://github.com/nerdalert/networkstatic-site`; production cutover remains separate. No production CNAME or DNS records have been changed.

## Review and operations

Run `make build-review HUGO=/opt/homebrew/bin/hugo-0.170.0` for the isolated `noindex` review site. The local preview at `http://localhost:1313/` serves published review content. Run `python3 scripts/prepare_publishable_content.py` to materialize only ledger-approved sources and owned media into the production Hugo roots.

Run `make build-staging HUGO=/opt/homebrew/bin/hugo-0.170.0` to validate the project-subpath build, route/search/feed/sitemap membership, `noindex`, repository output and security scans. See [docs/operations.md](docs/operations.md), [docs/migration.md](docs/migration.md), [reports/migration-exceptions.md](reports/migration-exceptions.md), and the machine-readable reports under `reports/` for evidence and per-article exceptions.

The full upload candidate inventory and all review source/output remain gitignored. Only media referenced by approved public pages is copied into the production site.
