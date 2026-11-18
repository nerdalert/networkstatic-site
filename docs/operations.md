# Operations

## Local review

Run `make build-review HUGO=/opt/homebrew/bin/hugo-0.170.0` to regenerate draft-flagged review output for the 190 public backup sources plus the verified April live-only article. The migration allowlist is exactly `post_type in ('post','page')`, `post_status == 'publish'`, and empty `post_password`. The review build verifies provenance, conversion fidelity, recovery reports, `noindex`, routes, search membership, media, output size and security. Its isolated preview is available at `http://localhost:1313/`.

## Production content and staging

`reports/publication-eligibility.csv` is the source allowlist. All 191 verified public/unprotected pages currently pass automated conversion checks. `scripts/prepare_publishable_content.py` copies only those ledger-approved pages and their owned media into Hugo's tracked `content/` and `static/` roots. It removes only migration-generated files from earlier runs and preserves utility pages and unrelated static assets. It validates source hashes, route equality, media hashes and the source audit before copying.

Build staging with the actual Pages project URL:

```sh
make build-staging HUGO=/opt/homebrew/bin/hugo-0.170.0
```

The successful local staging audit reports 519 HTML pages, all `noindex`; all 191 migrated routes in the search index and sitemap; 113 feeds with 1,179 feed items; zero broken local references; and about 308 MB of output. `reports/staging-local-audit.json` records the route and output evidence. `reports/conversion-fidelity.csv`, `reports/live-content-comparison.csv`, `reports/external-link-exceptions.csv`, and `reports/missing-media-recovery.csv` record the accepted content/media differences.

The Pages workflow uses the base URL returned by `actions/configure-pages`, pins Hugo and CleanWhite, runs the same route and security audits, uploads the artifact, and deploys to Pages. Staging stays `noindex`. It has no production CNAME, and no DNS changes are part of staging.

## Security and source handling

The original SQL, uploads, tar archive, full asset-candidate inventory, live crawl bodies, and converted review tree remain outside Git. The tracked production media set is limited to dependencies of eligible public sources plus the user-provided profile image. The audit confirms 55 nonpublic backup rows excluded, zero password-protected published rows, zero draft-only media copied, and no secret findings across repository files, staged blobs, Git history and generated staging output.
