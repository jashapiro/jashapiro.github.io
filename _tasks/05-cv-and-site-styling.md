# Task 05 — Consistent styling: fold CV CSS into site SCSS

## Goal

One coherent visual style across all pages, driven entirely from `css/shapbio.scss`
with CV-specific additions. The standalone `css/cv.css` is removed.

## Current state

- `css/cv.css` (26 lines) defines `.self`, `.species`, `.journal`, `.issue`, `.pages`,
  `li.pub` (hanging indent), `.bullets`, `.tight`. Referenced by `cv.qmd` front
  matter (`css: css/cv.css`). Not wired into `auto_cv.qmd` yet.
- `css/shapbio.scss` handles `figure.boxed`, `.pull-left/.pull-right`, `.file-link`
  and is the global theme overlay (`_quarto.yml` `theme: [litera, css/shapbio.scss]`).
- The `cv/` directory (external CSS themes: kjhealy, davewhipp, blmoore) is removed
  in task 01 — those are not the reference anymore.

## Design direction

The CV should inherit the main site's `litera` Bootstrap theme (fonts, spacing,
palette) and add only CV-specific overrides. Scope them to CV sections by id or
a body class to avoid polluting other pages. No separate stylesheet; everything
in `css/shapbio.scss`.

## Steps

- [ ] **Move `css/cv.css` rules into `css/shapbio.scss`** under a comment block
  `/* CV-specific styles */`. Review each rule:

  - `.self` (bold, for the author's name in pub lists) → keep as-is or scope to
    `#publications .self` if there's risk of collision.
  - `.species` (italic) → keep; used in both CV and research pages.
  - `.journal` (italic), `.issue` (bold), `.pages` → keep as-is.
  - `li.pub` (hanging-indent bibliography list items) → keep; scope to `#publications`
    or a `.pub-list` class if desired.
  - `.bullets` / `.tight` (research interests list) → keep.
  - Adjust margins/spacing to harmonise with `litera` defaults rather than the
    Bootstrap 3 values in the old `css/cv.css`.

- [ ] **Remove `css: css/cv.css`** from `cv.qmd`'s front matter — the rules are now
  global via `shapbio.scss`.

- [ ] **Ensure `auto_cv.qmd` picks up the same rules** — since it inherits the global
  theme, no per-file CSS reference is needed after the move.

- [ ] **Visual check** — after rendering, inspect:
  - CV page: publication list hanging indent, `.self` bold, `.species` italic,
    journal/issue formatting.
  - Research page: `figure.boxed`, `.pull-left/.pull-right` image floats.
  - Teaching page: `.file-link` bracketed file annotations.
  - About/index: headshot sizing/float (`.pull-left` + Bootstrap width attribute).

- [ ] **Remove `css/cv.css`** from the repo once everything looks correct.

## Files changed

`css/shapbio.scss` (additions), `cv.qmd` (remove `css:` front matter key),
deleted: `css/cv.css`

## Done when

- Both CV pages (`cv.qmd` and `auto_cv.qmd`) look visually correct with no separate
  stylesheet.
- All other pages render unchanged.
- `css/cv.css` is no longer tracked in git.
- No Quarto warnings about missing stylesheets.
