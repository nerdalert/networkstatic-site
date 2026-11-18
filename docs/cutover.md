# Production deployment and DNS status

The user configured GitHub Pages for `networkstatic.net` and reports the DNS change is active. Independent DNS checks show the apex records point to GitHub Pages and `www` points to `nerdalert.github.io`; the MX record remains `smtp-fwd.wordpress.com`. No DNS or mail records were changed by this migration.

The production build uses `https://networkstatic.net/` as its Hugo base URL. It removes staging `noindex`, emits root-path assets and internal links, and does not add a `CNAME` file. The existing GitHub Pages custom-domain setting supplies the domain. The former project-subpath staging output at `/networkstatic-site/` is obsolete and must not be linked from the production site.

The production build is deployed from commit `d853b67a7020af72309fcac9e884b4b0f0f67b7c`; the successful Pages workflow is [run 44227290680](https://github.com/nerdalert/networkstatic-site/actions/runs/44227290680). The live site is [https://networkstatic.net/](https://networkstatic.net/). GitHub Pages has the `networkstatic.net` custom domain, an approved certificate, and HTTPS enforcement enabled. HTTP and `www` both redirect to the apex HTTPS URL.

The production build contains 514 HTML files, 190 migrated post/page routes, 190 search records, 111 RSS feeds with 1,169 items, one sitemap, zero `noindex` pages, zero broken local references, and zero security findings. See `reports/production-local-audit.json` for the full route and output audit. Browser and remote HTTP validation is recorded in `reports/migration-exceptions.md`.

The old WordPress site remains available for rollback. Preserve the WordPress.com registration, renewal and nameserver settings, and do not change email routing. No DNS, MX, or mail records were changed by this migration.

GitHub Pages does not provide arbitrary HTTP redirects. Exact eligible post paths are preserved. Unsupported historical query/feed routes require a separate redirect plan.
