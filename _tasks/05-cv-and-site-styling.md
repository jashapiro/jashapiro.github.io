# Task 05 — Consistent styling: retire css/cv.css

> **Status (2026-10-24):** replanned and shrunk, following the task 04 rewrite. Once the
> CV renders its publications through citeproc and its other sections as plain
> markdown, none of the `css/cv.css` span classes are used. Do this after task 04.

## Goal

One coherent visual style across all pages, driven entirely from `css/shapbio.scss`.
The standalone `css/cv.css` is removed.

## Current state

- `css/cv.css` (26 lines) styles `ul` (no bullets, inside position), `li.pub` (hanging
  indent), `.self`, `.species`, `.journal`, `.issue`. All of these classes are used only
  in `cv.qmd` (checked 2026-10-24; the research page does not use `.species`).
- After task 04:
  - publications come from citeproc: `.csl-entry` divs, hanging indent from the
    CSL `hanging-indent="true"`, own name bolded by a Lua filter (`Strong`), titles
    italicized from `\textit{}` in `papers.bib`;
  - Experience / Education / Honors are plain markdown lists with `*...*` italics.
- `css/shapbio.scss` is the global theme overlay on Bootstrap `litera`.

## Steps

- [ ] Remove `css: css/cv.css` from `cv.qmd`'s front matter and delete `css/cv.css`.
- [ ] Render and look at the CV HTML. Add only what's still needed to
  `css/shapbio.scss` under a `/* CV */` comment, scoped to the CV (e.g. `#refs` or a
  page class), e.g. spacing between `.csl-entry` items or list bullets. Use `litera`
  defaults where possible.
- [ ] Check the Typst PDF separately; it doesn't use the site CSS, so any PDF tweaks
  belong in `cv.qmd`'s `typst` format options.
- [ ] Spot-check the other pages are unchanged (research `figure.boxed` and floats,
  teaching `.file-link`, about headshot `.pull-left`).
- [ ] Update `AGENTS.md` (Styling section) to drop `css/cv.css`.

## Files changed

`cv.qmd` (front matter), `css/shapbio.scss` (small CV additions if any), `AGENTS.md`;
deleted: `css/cv.css`.

## Done when

- The CV looks right with no separate stylesheet, and other pages render unchanged.
- `css/cv.css` is no longer tracked in git.
