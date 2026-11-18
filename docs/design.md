# Design and theme record

## Required starting point

The required starting theme is [Hugo Theme CleanWhite](https://github.com/zhaohuabing/hugo-theme-cleanwhite), pinned to commit `c4c7f2171e4c8244a8588fd6a101c48154ae1229` (upstream history shows the abbreviated commit `c4c7f21`, dated April 2, 2025). Its repository license is Apache-2.0 and notes that some inherited components have separate notices. Preserve upstream notices with the theme checkout.

The upstream README documents comments, Algolia, analytics, reward widgets, video embeds and a built-in dark mode. NetworkStatic will keep comments, trackers, donations and hosted search disabled. The automatic time-of-day theme switch will be disabled; styling will use NetworkStatic navy/slate and blue accents with readable light/dark surfaces.

## NetworkStatic sidebar

The home page, archive, search, taxonomy, author, and article layouts use a right-hand CleanWhite-style sidebar. It shows the user-provided Brent Salisbury portrait, the requested short bio, and round LinkedIn, X, and GitHub icons. Bluesky is omitted because the pinned theme's icon set does not include it. The portrait is listed as an explicitly owned site-wide asset in `reports/site-ui-assets.csv`.

## Implementation status

The pinned CleanWhite checkout is installed at `c4c7f2171e4c8244a8588fd6a101c48154ae1229`, and Hugo 0.170.0 builds run successfully. The home page and article layouts were visually reviewed locally and on deployed staging; the right sidebar shows the user-provided portrait, the approved bio, and LinkedIn, X, and GitHub icons. Bluesky is omitted. The local project-subpath staging build and GitHub Pages deployment pass route, noindex, and security audits. Deployment details and remote checks are recorded in `reports/migration-exceptions.md`.
