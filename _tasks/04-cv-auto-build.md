# Task 04 — Complete the auto CV

## Goal

`auto_cv.qmd` becomes a full, rendered CV covering all sections: education,
employment, publications, research interests, presentations, and honors. Once
trusted, it replaces `cv.qmd` in the navbar.

## Current state

`auto_cv.qmd` fetches education, employment, and publication data from ORCID
(id `0000-0002-6224-0347`) via `rorcid`, but those chunks are all `include: false`
and their results are **never printed**. The only visible output is the bibliography
from `vitae::bibliography_entries("papers.bib", "Publications")`.

## Design decisions (already settled)

- **Publications** come from the committed `papers.bib` (14 entries, more complete
  than the 9 hard-coded in `cv.qmd`). Rendered via `vitae::bibliography_entries()`.
  No live call at render time.
- **Education/employment** come from ORCID via `rorcid`. Freeze the page so the live
  ORCID call (needs `.httr-oauth`) is only made locally; CI renders from `_freeze`.
- **Static sections** (Research Interests, Presentations, Honors) cannot come from
  ORCID; port them from `cv.qmd`.
- The page stays in the site's normal `format: html` (inherited from `_quarto.yml`).
  `vitae::markdowncv` output format does **not** integrate with a Quarto website.
- Styling (`.self`, `.species`, `.journal`, `.pub`, etc.) comes from the site SCSS
  (task 05 moves these there from `css/cv.css`). For now, `css/cv.css` can still be
  referenced in the front matter during development.

## Steps

- [ ] **Render the education data frame.** Replace the `#| include: false` on the
  `education` chunk (or add a new chunk after it) that emits the education as HTML —
  either a simple loop/`knitr::kable` or using `vitae::detailed_entries()` and then
  styling its output. Columns to show: degree, school, department, city/state, year.

- [ ] **Render the employment data frame** similarly — title, org, dept, city/state,
  start/end dates.

- [ ] **Port static sections from `cv.qmd`:**
  - Research Interests (`#summary`) — the four bullet points.
  - Presentations (`#presentations`) — 10 conference items.
  - Honors & Awards (`#honors`) — 8 items.
  These can be copied as-is (Pandoc HTML/markdown) since `auto_cv.qmd` renders as
  standard Quarto HTML.

- [ ] **Freeze the page.** Add `freeze: true` to `auto_cv.qmd`'s front matter (or
  create `_metadata.yml` in the root if other root-level pages also need it). Run a
  local render (with `.httr-oauth` present) to populate `_freeze/auto_cv/...`, then
  commit the freeze output.

- [ ] **Wire into the navbar.** In `_quarto.yml`, change the `cv` dropdown entry from
  `cv.qmd` to `auto_cv.qmd`. Leave `cv.qmd` in the repo but unlinked as fallback.

- [ ] **Update `renv.lock`** if any new packages are added during development (run
  `renv::snapshot()` and commit the updated lockfile).

## Files changed

`auto_cv.qmd`, `_quarto.yml`, `_freeze/auto_cv/...` (new freeze output),
possibly `renv.lock`

## Done when

- The linked CV page shows: Research Interests, Education, Employment, Publications
  (bibliography), Presentations, Honors.
- `quarto render` reproduces the CV from `_freeze` with no live ORCID call.
- The navbar "cv" entry points to `auto_cv.qmd`.
