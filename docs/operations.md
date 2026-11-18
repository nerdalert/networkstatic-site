# Build and publication

## Local review

Run `make build-review HUGO=/opt/homebrew/bin/hugo-0.170.0` to build the isolated, `noindex` review site. The migration allowlist requires `post_type in ('post','page')`, `post_status == 'publish'`, and an empty `post_password`; route-level exclusions are in `config/publication-exclusions.csv`. The review build checks source provenance, conversion fidelity, recovery reports, routes, search membership, media, and security. Its local preview is available at `http://localhost:1313/`.

## Production preview and deployment

Run `make build-production-preview HUGO=/opt/homebrew/bin/hugo-0.170.0` to build and audit the root-path production site locally. The Pages workflow uses Hugo 0.170.0 and the pinned CleanWhite theme, builds with `https://networkstatic.net/`, then audits the generated routes, search index, RSS feeds, sitemap, canonical URLs, noindex metadata, media references, and security before deploying.

The current production preview contains 514 HTML files, including 183 posts and 7 migrated pages; 190 eligible migrated routes appear in search. It has 111 RSS feeds with 1,169 items, one sitemap, zero `noindex` pages, zero broken local references, and zero security findings. Output is about 306 MB. `reports/production-local-audit.json` records these checks.

`make build-staging HUGO=/opt/homebrew/bin/hugo-0.170.0` remains available for a local project-subpath staging preview. It is not the GitHub Pages deployment target. The deployed site uses the custom-domain root and has no staging `noindex`.

## Content and security

`reports/publication-eligibility.csv` approves 190 public, unprotected pages. `scripts/prepare_publishable_content.py` copies only ledger-approved pages and their owned media into Hugo's tracked `content/` and `static/` roots. It removes only migration-generated files from earlier runs and preserves utility pages and unrelated static assets. It validates source hashes, route equality, media hashes, and the source audit before copying.

The original SQL dump, upload archive, full asset-candidate inventory, live crawl bodies, and converted review tree remain outside Git. Tracked migration media is limited to eligible public content dependencies and the profile image. Audits confirm 55 nonpublic backup rows excluded, zero published password-protected rows, zero draft-only media copied, and no secret findings across repository files, staged blobs, Git history, or generated production output.

The accepted content and media differences are listed in `reports/conversion-fidelity.csv`, `reports/live-content-comparison.csv`, `reports/external-link-exceptions.csv`, and `reports/missing-media-recovery.csv`.
