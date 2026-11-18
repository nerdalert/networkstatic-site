# Praxis Grid review source

The checksum-verified package from `praxis-grid-blog.zip` is preserved unchanged in [`praxis-grid-blog-package/`](praxis-grid-blog-package/). It contains the research notes, source article, regeneration scripts, editable DOT diagrams, SVG exports, and original PNG renders.

The Hugo review copy is [`content/posts/praxis-grid-distributed-ai-inference-routing/index.md`](../../content/posts/praxis-grid-distributed-ai-inference-routing/index.md). It is a draft and uses only the seven PNGs referenced by the article. To build a separate local review output, run `make build-draft-preview HUGO=/opt/homebrew/bin/hugo-0.170.0`, then serve `public-draft-preview` on port 1315. The normal production build excludes the draft and its companion source-notes page.

The bundled `render_diagrams.py` and `validate_assets.py` remain in the preserved source package. Diagram generation is not part of the regular production build.
