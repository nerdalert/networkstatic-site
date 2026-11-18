# Rollback proposal

Production cutover has not occurred, so there is no migration DNS change to reverse. Keep the WordPress host and backup intact until a later cutover is approved and validated.

If a future cutover fails, restore the recorded pre-cutover A/AAAA/CNAME values, keep MX and email authentication records untouched, and allow DNS caches to expire according to the prior TTL. Re-enable or retain WordPress at the original paths. Keep the Pages build available for diagnosis, but do not remove or repoint the production domain until DNS and URL checks pass.

Abort cutover if migrated paths, media, code, taxonomies, canonical host, feed behavior or HTTPS cannot be verified. GitHub Pages static alias files are client-side behavior and do not replace true 301 redirects.
