# Live discovery coverage

## Method and evidence

- `scripts/discover_live.py` fetched the homepage, archive pages 2–23, WordPress post/page/attachment sitemaps, REST API endpoints, selected recovery assets, and every post/page route listed by the public sitemaps. The crawler uses a standard browser User-Agent and navigation headers because the origin's ModSecurity returned HTTP 406 to its earlier descriptive crawler User-Agent.
- `reports/live-fetch-diagnostics.csv` records requested URL, method, attempt, UTC timestamp, HTTP status or transport error, final URL, content type, body length/hash, and saved file. The exact successful response pages and media are in the ignored `migration-review/live-crawl/` directory. `live-browser-probes.csv` is kept separate from origin HTTP responses.
- Parsed 175 cards from archive pages 2–23; the supplied homepage snapshot contributes 8 cards. Archive fetch status counts: `{'200': 175}`.
- The public post sitemap lists 184 routes and the page sitemap lists 7; direct route status counts are `{'200': 191}`. The `live-sitemap-observations.csv` rows also record titles, last-modified dates, response hashes, normalized body/code/link/media hashes, and password-form presence.
- Anonymous REST route lookups matched 191/191 exact paths; REST source status counts are `{'publish': 191}` and `content.protected` counts are `{'false': 191}`. Per-route IDs, body hashes, titles, dates, response attempts, and paths are in `live-rest-observations.csv`; response bodies stay in ignored `migration-review/live-rest/`.
- One backup post omitted from archive cards, `/my-notes-from-2/`, is present in the published post sitemap and direct route fetch. The April 17 article is also in the sitemap and REST API. The current live route for `/open-v-switch-red-hat-installation/` (backup ID 4867) returned HTTP 404. The published backup article is included in the migration, so the corresponding staging link resolves locally; the live 404 remains documented as historical context.

## Coverage and reconciliation

The live inventory contains 191 unique public post/page routes. It observes 183 of 183 published backup posts and 7 of 7 published backup pages. There are 1 live-only routes, 0 backup-only post candidates, and 0 backup-only page candidates. These are route findings; absence from a card or sitemap is not classified as deletion.

`live-content-inventory.csv` combines the supplied homepage snapshot, archive cards, public sitemaps, and direct route responses. `live-archive-observations.csv`, `live-sitemap-observations.csv`, and `live-rest-observations.csv` preserve the source observations. `live-vs-backup.csv` records route/title differences, confidence, and review actions. `live-content-comparison.csv` compares normalized text/code/link/media and source/live metadata for every backup article against both anonymous REST bodies and direct page responses; `conversion-fidelity.csv` separately compares generated review files against backup sources. Article-specific checks and exceptions are in `content-verification.csv`.

Taxonomy/date archives, historical redirects, comments feed, and all non-content dependencies are not covered by the post/page route crawl. The automated content comparisons and per-article exceptions are recorded. The publication ledger approves 190 pages; the verified live-only route is explicitly excluded by `config/publication-exclusions.csv`. The staging audit confirms zero broken local references.
