# Backup/live reconciliation

The machine-readable `live-vs-backup.csv` contains one row per unique live route and each published backup post/page. Evidence includes route/title observations, confidence, and a follow-up action. Archive card presence establishes a listed route; sitemap/direct-route observations establish public availability, not content parity.

| Classification | Count | Confidence | Evidence/action |
|---|---:|---|---|
| `route-and-title-match-only` | 172 | medium | Route and title match a directly observed page; full body comparison is reported separately. |
| `route-match-title-differs` | 18 | low | Route matches, but the live title differs from backup; the user accepted these differences for publication and each remains recorded. |
| `live-only` | 1 | high | A live-only route is fully verified against the public REST response and page; route-level policy excludes it from review and production output. |
| `backup-only-candidate-review` | 0 | low | No published backup routes were absent from the observed published sitemap. |
| `backup-page-unobserved-review` | 0 | low | No published backup pages were absent from the observed page sitemap. |

Discovery observed the homepage and archive pages 2–23, the public post/page sitemaps, and direct HTTP status for all 191 listed routes. All 190 backup routes are represented in the sitemaps. No unobserved route is classified as deleted. Per-article text, code, links and media comparisons are in `live-content-comparison.csv`; body differences were accepted as nonblocking and remain documented. The publication ledger approves 190 backup sources; the one live-only route is excluded by `config/publication-exclusions.csv`.

The live-only route's public status, unprotected state, full content, and six image files are recorded in `content-verification.csv`, `live-source-eligibility.csv`, and `live-recovered-media.csv`. Its page and exclusive media are excluded from the production output.
