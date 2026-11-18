# Live content comparison

Compared 190 public, unprotected backup post/page sources with directly fetched live routes and their anonymous WordPress REST bodies.
Text, code, link, media and title exact counts: `{'title_exact': 172, 'body_text_exact': 7, 'code_exact': 143, 'links_exact': 108, 'media_exact': 110}`.
Full body matches (text/code/links/media): 6/190.
Live REST status and password checks passed for 190/190 (`status=publish`) and 190/190 (`content.protected=false`). Direct-page versus REST normalized text/code/link matches are `{'live_rest_vs_page_text_exact': 190, 'live_rest_vs_page_code_exact': 188, 'live_rest_vs_page_links_exact': 190}`.
REST rows also record live post ID, exact route match, body hash, and modified date. A live-versus-backup mismatch is not automatically a conversion loss; `conversion-fidelity.csv` separately compares every converted review page with its backup source. Six per-article local link exceptions and three external-media exceptions remain documented.
The April 17 live-only post is not included in the backup-row totals; its public REST/page comparison and six image hashes are verified in `content-verification.csv`, `live-source-eligibility.csv`, and `live-recovered-media.csv`.
