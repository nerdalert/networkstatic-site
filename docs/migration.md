# Migration method and provenance

## Source and handling

The source is a cPanel-style account backup folder and a matching POSIX tar archive in the parent Downloads directory. The SQL source is `mysql/bbsali0_wrdp1.sql`; its table prefix is `wp_`. The archive was inventoried but not extracted in this workflow, and no PHP from the backup is executed. Raw SQL and the tar stay outside this repository.

The inventory parser reads MySQL `INSERT` statements without importing a database. It parses quote/escape-aware rows and keeps distinct outputs for eligible public WordPress posts/pages, observed public routes, and attachment-file candidates. The migration allowlist is exactly `post_type in ('post', 'page')`, `post_status == 'publish'`, and empty `post_password`. Draft, auto-draft, pending, private, trash, revision, and password-protected content is excluded. Excluded status counts are reported without titles or content.

## Field mapping

| WordPress source | Hugo target |
| --- | --- |
| `post_title` | `title` |
| `post_date` | `date`, retaining the source UTC offset (`+00:00`) |
| `post_modified` | `lastmod` |
| `post_author` → `wp_users.display_name` | `author` |
| `post_name` | Filename/route slug |
| `post_excerpt` | `description` |
| `category` / `post_tag` relations | `categories` / `tags` |
| `ID` | `wp_id` |
| Original permalink | `permalink`, with Hugo routes set to preserve `/<slug>/` |

The `guid` is not used to infer a canonical URL. Conversion and publication eligibility are separate: every allowed public source is deterministically converted into an ignored local review tree with Hugo `draft = true` and `review_only = true`. Automated text, code and link comparisons must pass. Exact media parity or an article-specific documented media exception is accepted. Manual live parity review and title differences are recorded but do not block otherwise passing published content. `reports/publication-eligibility.csv` records the per-article decision; `reports/link-exceptions.csv` records link-level exceptions. Links between eligible migration pages resolve as normal site dependencies.

## Live versus backup

`reports/live-archive-observations.csv` records 175 cards observed across archive pages 2–23; the supplied homepage snapshot adds 8 cards. The public post/page sitemaps list 184 and 7 routes, and all 191 route GETs returned HTTP 200. `reports/live-fetch-diagnostics.csv` and `reports/live-browser-probes.csv` preserve request methods, statuses/errors, and retry/cache notes. `reports/live-vs-backup.csv` gives path/title evidence and confidence per row, not a deletion finding. All 190 backup routes are represented in the live sitemaps; 18 titles differ from the backup. The direct route bodies and the backup-derived output are compared separately. A route/title match alone does not establish content parity.

One live-only route was fully verified against the anonymous WordPress REST response and direct article page. Its source status, password flag, body, links, and six images are documented in `reports/live-source-eligibility.csv`, `reports/live-recovered-media.csv`, and `reports/content-verification.csv`. `config/publication-exclusions.csv` excludes that route from review and production output; its exclusive images are not copied into the site.

## Shortcodes

`reports/shortcode-inventory.csv` lists tags statically found in the captured backup PHP source. `reports/shortcode-tag-observations.csv` records bracket-token counts from eligible published content; these counts can include code examples and are not proof every token is a shortcode. The converter handles legacy heading, figure, list, quote, callout, code, link and video forms. Presentation fallbacks are recorded by article; review, staging and production audits reject any remaining raw shortcode syntax outside code.

## Media

The inventory hashes and measures every file under uploads and records literal source references/owners. Conversion copies only dependencies of eligible public sources; the source audit rejects media used exclusively by excluded sources. Automated media comparison checks dependency sets and copied-file hashes. A repeatable recovery pass attempted all 17 media files absent from the backup: 14 images were fetched and hashed; three files remained unavailable. The unavailable traffic image was an empty anchor shell and was removed without losing visible text. Two unavailable PDFs remain external links and are listed in `reports/external-link-exceptions.csv`; per-attempt statuses are in `reports/missing-media-fetch-diagnostics.csv`. Full inventory paths remain in the gitignored local `asset-candidates.csv`.

## Current local validation

All 190 backup sources pass text, code and link comparisons. Media is exact for 187; the remaining three pages pass with documented media-only exceptions. The 18 live title differences and body discrepancies are accepted and documented. Four broken attachment-page references now point to their backed-up media files; the malformed Docker Machine URL is corrected; the historical OVS link is preserved as an external WordPress link. The production build uses `https://networkstatic.net/`, audits root-path links and assets, and excludes the configured live-only route. The user reports DNS is active; no DNS or email records were changed by the migration.
