# Production cutover proposal — NOT EXECUTED

The user supplied the production plan: set GitHub Pages custom domain to `networkstatic.net`; build Hugo at `https://networkstatic.net/` with staging `noindex` removed; and update website records at HostGator after resolving the email MX dependency. Keep the WordPress.com portal, registration, renewal, and custom nameservers unchanged. Keep the old WordPress site available initially for rollback.

No custom domain, production URL, DNS record, email record, TLS setting, or WordPress service has been changed. Staging remains at `https://nerdalert.github.io/networkstatic-site/` with `noindex` enabled.

After staging has been deployed and verified, cutover requires a separate reviewed change plan:

1. Confirm the current apex, `www`, MX, SPF, DKIM, DMARC and other HostGator DNS values. Resolve and verify the email MX dependency before changing website records; preserve every unrelated record.
2. Configure `networkstatic.net` in the Pages repository and production Hugo base URL. Use the current GitHub Pages instructions to confirm required apex and `www` records and certificate status.
3. Prepare a reversible DNS diff with previous values and rollback steps. Apply only website records at HostGator; retain WordPress.com registration, renewal and nameserver settings.
4. Remove staging `noindex` and switch production canonicals/sitemap to `https://networkstatic.net/` only in the production build.
5. Verify HTTPS, apex and `www`, representative article routes, media, RSS, robots/noindex, canonical URLs and sitemap. Keep the old WordPress service available during the initial validation window.

GitHub Pages does not provide arbitrary HTTP redirects. Exact post paths are preserved; unsupported historical query/feed routes require a separate redirect plan. This proposal is not authorization to execute cutover as part of staging.
