# Praxis Grid blog post — ready-to-review package

A complete Markdown article and seven locally hosted, editable diagrams. Nothing is published or committed from this package.

## Contents

```text
praxis-grid-blog/
├── README.md                  # This file
├── article.md                 # Full, frontmatter-ready blog post
├── source-notes.md            # Pin revisions, evidence, limitations
├── assets/
│   ├── 01-praxis-family.png   # PNG renders used by article.md
│   ├── 01-praxis-family.svg   # Vector exports for optional reuse
│   └── ... 02 through 07
├── diagrams/
│   ├── 01-praxis-family.dot   # Editable Graphviz source
│   └── ... 02 through 07
└── scripts/
    ├── render_diagrams.py    # Deterministic SVG + PNG re-render
    └── validate_assets.py    # Markdown image/link, PNG checks
```

## Editorial angle

The article first explains the Praxis project boundaries, then uses a realistic multi-site inference example to walk from **authorization and placement** through **admission, pressure, affinity, and secure provider hops**. It distinguishes the Grid operator's offline decisions from the gateway request path; the overlay-based `intelligent_route` and Grid-serving `grid_site_route` modes; and pool selection from llm-d/Dynamo worker scheduling. It treats consistency, failure, opt-in configuration requirements, and agentic delegation as operating contracts rather than marketing claims.

## Asset generation

All images are checked in as relative paths: `![...](assets/NN-name.png)`. They work in Markdown viewers that support ordinary relative images, including GitHub, without hosted assets or Mermaid rendering.

Requirements:

- Python 3.10 or later
- Graphviz CLI (`dot` in `PATH`)
- Pillow (`python3 -m pip install pillow`)
- A system font providing **DejaVu Sans** for the supplied layout (or substitute an installed font in `.dot` sources)

From the package root:

```bash
python3 scripts/render_diagrams.py
python3 scripts/validate_assets.py
```

To edit a diagram, modify its `diagrams/NN-name.dot` file, then re-render. The script emits a companion SVG and a blog-friendly, 2,000-pixel-wide RGB PNG. The DOT source is the authoritative editable asset; SVG is an additional editable vector format if preferred.

## Suggested publication workflow

1. Read the article and [research notes](source-notes.md), especially the draining, external tenant authorization, and quota and accounting caveats.
2. Confirm the target site's Markdown frontmatter syntax and theme (the YAML fields are generic and work with most static-site generators).
3. Copy the entire folder into your content repository or move the `article.md` and `assets/` directory together. If you change the directory arrangement, adjust relative links.
4. Review generated previews at normal article width, with particular attention to longer node labels and mobile screens.
5. Publish only after the release-specific source and operational caveats are acceptable.

**Caveat:** The bundled revision links document the code reviewed on November 17, 2026. No live systems, GitHub commits, release tags, or performance suites were modified or executed for this deliverable.
