# Task 02 — Keep old course links working

## Goal

Preserve `/courses/...` URLs that still have content. The old Jekyll site had no
redirect machinery, so URLs survive only by keeping output paths byte-identical to
what Jekyll produced.

## Problem

1. `courses/biolB215s19/index.markdown` has a Jekyll `layout: page` front matter and
   a `.markdown` extension. Quarto does not render `.markdown` files by default, so
   `/courses/biolB215s19/` — which `teaching.qmd` links to — will 404 as-is.

2. `courses/biolB216s14/` has no index file at all, so `/courses/biolB216s14/` 404s.

3. The `f14/f15/s13/s14/s18` course tutorial pages were intentionally removed in a
   prior commit ("remove old biostat courses"); only their syllabus PDFs remain. This
   is accepted breakage — document it here and leave it.

## Steps

- [ ] Convert `courses/biolB215s19/index.markdown` → `courses/biolB215s19/index.qmd`.
  - Strip Jekyll front matter keys (`layout`, `pretitle`, `nav`).
  - Keep `title: Experimental Design and Statistics` (and `pretitle` as a subtitle
    if wanted, or drop it).
  - All relative links in the body (`install_orient.html`, `first_steps.html`,
    `dataframes.html`, `list_matrix.html`, `graphics.html`, `capture_recapture.html`,
    `abalone_cleaning.html`, `BiolB215_syllabus_Sp2019.pdf`) resolve to the same
    output paths — no changes to the link text needed.
  - Delete the old `index.markdown` file.

- [ ] Add a minimal `courses/biolB216s14/index.qmd`:
  ```yaml
  ---
  title: Introduction to Genomics — Computational Lab (Spring 2014)
  ---
  ```
  With a link to `darwinAssembly.html` — matching the structure that existed on the
  old Jekyll site's `biolB216s14` index.

- [ ] Confirm in `_site/` after a render:
  - `_site/courses/biolB215s19/index.html` exists.
  - Each tutorial `_site/courses/biolB215s19/<name>.html` exists (these come from
    the frozen `.Rmd` → `.html` pipeline already committed in `_freeze/`).
  - `_site/courses/biolB216s14/index.html` and `darwinAssembly.html` exist.
  - All course syllabus PDFs are copied verbatim to their original paths.

- [ ] **Document accepted URL gaps** (these will 404 — by design):
  - `/courses/biolB215f14/<tutorial>.html`
  - `/courses/biolB215f15/<tutorial>.html`
  - `/courses/biolB215s13/<tutorial>.html`
  - `/courses/biolB215s14/<tutorial>.html`
  - `/courses/biolB215s18/<tutorial>.html`
  Syllabus PDFs for those years are still served (the PDF files remain in the
  respective course dirs).

## Files changed

`courses/biolB215s19/index.markdown` → deleted; new `courses/biolB215s19/index.qmd`,
new `courses/biolB216s14/index.qmd`

## Done when

- `/courses/biolB215s19/` and every linked tutorial `.html` render at their original
  paths.
- `teaching.qmd`'s `courses/biolB215s19/index.html` link resolves in the built site.
- `/courses/biolB216s14/index.html` exists.
