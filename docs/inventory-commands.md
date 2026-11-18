# Inventory and migration commands

Run these commands from the `networkstatic-site` directory. The SQL dump and uploads remain in the neighboring backup directory. The original backup is read-only throughout this workflow.

## Live discovery diagnostics

```sh
python3 scripts/discover_live.py --retries 1 --timeout 6
```

The script requests the homepage, archive routes, observed articles, sitemap/REST/feed endpoints, and the April 17 article. It writes every attempt to `reports/live-fetch-diagnostics.csv`, including requested URL, retrieval method, attempt number, HTTP status or transport error, response hash, and retry outcome. Successful page bodies stay under ignored `migration-review/live-crawl/`. Browser fetch observations and cache notes from the available browser tool are separately preserved in `reports/live-browser-probes.csv`. Tool-level cache/fetch failures are not presented as confirmed origin responses.

## Backup inventory and reconciliation

```sh
./scripts/inventory.py \
  --sql ../backup-4.10.2023_17-56-43_bbsali0/mysql/bbsali0_wrdp1.sql \
  --uploads ../backup-4.10.2023_17-56-43_bbsali0/homedir/public_html/wp-content/uploads \
  --homepage ../networkstatic.net.html \
  --live-archive reports/live-archive-observations.csv \
  --fetch-diagnostics reports/live-fetch-diagnostics.csv \
  --browser-probes reports/live-browser-probes.csv \
  --wp-root ../backup-4.10.2023_17-56-43_bbsali0/homedir/public_html/wp-content \
  --archive '../backup-4.10.2023_17-56-43_bbsali0 2.tar'
```

The parser reads MySQL `INSERT` statements without importing a database, executing PHP, or extracting the tar. Backup content inventories include only WordPress `post`/`page` rows with exactly `post_status == "publish"` and an empty `post_password`. `reports/source-eligibility.json` records aggregate excluded counts by type/status and protected-row count without excluded titles or content.

`reports/backup-content-inventory.csv` is the independent backup-side inventory. `reports/live-content-inventory.csv` combines cards, sitemap routes, and direct page observations. The homepage and archive CSVs retain their source observations. `reports/live-vs-backup.csv` includes evidence and confidence for every observed route and eligible backup route. Absence from sampled routes means unobserved, not deleted.

Fetch and compare the public REST body for each sitemap route:

```sh
python3 scripts/fetch_live_rest.py --delay 0.2 --retries 2
python3 scripts/compare_live_content.py \
  --sql ../backup-4.10.2023_17-56-43_bbsali0/mysql/bbsali0_wrdp1.sql
```

`live-rest-observations.csv` records each exact route query, HTTP result, WordPress ID/type/status, `content.protected`, dates, and content hash; saved responses are ignored under `migration-review/live-rest/`. The current crawl matched 191/191 routes: all are `publish` and `content.protected=false`.

## Conversion, source audit, and fidelity comparison

```sh
python3 scripts/convert.py \
  --sql ../backup-4.10.2023_17-56-43_bbsali0/mysql/bbsali0_wrdp1.sql \
  --uploads ../backup-4.10.2023_17-56-43_bbsali0/homedir/public_html/wp-content/uploads

python3 scripts/import_live_recoveries.py

python3 scripts/audit_migration_sources.py \
  --sql ../backup-4.10.2023_17-56-43_bbsali0/mysql/bbsali0_wrdp1.sql \
  --uploads ../backup-4.10.2023_17-56-43_bbsali0/homedir/public_html/wp-content/uploads \
  --review-dir migration-review/generated

python3 scripts/compare_conversion.py \
  --sql ../backup-4.10.2023_17-56-43_bbsali0/mysql/bbsali0_wrdp1.sql \
  --uploads ../backup-4.10.2023_17-56-43_bbsali0/homedir/public_html/wp-content/uploads
```

Conversion creates deterministic Hugo draft files under ignored `migration-review/generated/`, never production `content/` or `static/`. Only public, unprotected backup sources enter review output. Link resolution is per article: a link to an excluded or unreconciled target is preserved and reported in `reports/link-exceptions.csv`; it does not import the target or block unrelated conversions. Copied media is limited to dependencies of eligible published sources.

The source audit proves one-to-one backup source coverage, published status, empty source password, matching source hashes, review-only Hugo flags, and no copied draft-only media. It separately validates the recovered April REST source and six hashed media files. Excluded reports expose counts only. The fidelity comparison records normalized text/hashes, code samples/hashes, links, media dependencies, ownership, copied-file presence and SHA-256 parity. Its result is in `reports/conversion-fidelity.csv`; live-versus-backup body results are separate in `reports/live-content-comparison.csv`. Backup fidelity does not itself approve publication.

## Current live coverage and limits

The homepage has 8 cards; archive pages 2–23 have 175 cards. The public post/page sitemaps and anonymous REST queries cover 191 unique routes (184 posts and 7 pages), all directly fetched with HTTP 200. The routes include every one of the 190 backup articles/pages and one live-only post. Eighteen titles differ from the backup; the REST comparison has exact body text on 7, code on 143, links on 108, and media on 110 of the 190 backup rows. The April 17 “ChatGPT your Project Docs” full-body, code-count, links, and media comparison passes and is in local review output. These figures and article-specific details are recorded in the generated reports; conversion fidelity to backup is a separate comparison.

## Build and audits

```sh
python3 -m py_compile scripts/*.py
make build-review HUGO=/opt/homebrew/bin/hugo-0.170.0
```

The latest isolated review build uses pinned Hugo 0.170.0 and CleanWhite, emits 184 backup/live-only posts and 7 backup pages under `migration-review/site`, disables feeds and sitemap, keeps `noindex`, validates the 191-source search allowlist, and scans repository, staged blobs, Git history, and output. Its route audit reports zero broken local references. The full local Pages-subpath build also passes with all 519 HTML pages `noindex`, 191 search records, validated feeds and sitemap, zero broken references, and no security findings. The publication ledger approves all 191 public/unprotected pages; detailed title/body/media exceptions remain in their separate reports.
