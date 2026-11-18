# NetworkStatic

NetworkStatic is Brent Salisbury's blog about networking, programming, and infrastructure. This repository contains the Hugo site and its posts. The production site is [networkstatic.net](https://networkstatic.net/).

## Instructions for AI writing assistants

When asked to prepare a post:

- Create a new file at `content/posts/<slug>.md`. Do not rewrite or remove existing posts unless asked.
- Write in a clear, practical first-person voice. Use only facts, opinions, experience, quotes, and results supplied or verified; never invent Brent's personal experience. Ask for missing facts that materially affect the article.
- Use Markdown and fenced code blocks with language labels. Preserve code meaning, add useful headings, and include accurate image alt text and captions.
- Keep the requested URL stable as `/<slug>/`. Use `{{< relurl "/existing-post/" >}}` for internal links so they work with both staging and production base URLs.
- Put new post images in `static/images/posts/<slug>/` and reference them with the `relurl` shortcode, for example `{{< relurl "/images/posts/<slug>/diagram.png" >}}`.
- Use TOML front matter in this shape. Use the date the user specifies; if none is given, use today's date in UTC.

  ```text
  +++
  title = "Post title"
  date = "YYYY-MM-DDTHH:MM:SS+00:00"
  author = "Brent Salisbury"
  categories = ["Networking"]
  tags = ["example"]
  description = "A concise summary of the post."
  url = "/post-slug/"
  draft = true
  +++
  ```

- Leave new posts as drafts unless the user explicitly asks to publish. For a requested publication, set `draft = false`. Do not add migration-only fields such as `wp_id`, `source_status`, `source_content_sha256`, or `migration_generated` to new posts.
- Respect the exclusions in `config/publication-exclusions.csv`; do not add excluded routes to the site.
- Do not change migrated post URLs, production-domain settings, or DNS unless explicitly asked. Pushing to `main` builds and deploys the production site through GitHub Actions.

## Build

The site uses Hugo 0.170.0 and the CleanWhite theme pinned in `THEME_COMMIT`. Run `make build-production-preview HUGO=/opt/homebrew/bin/hugo-0.170.0` to build and audit a local production preview.
