# Task 01 — Control render scope, remove Jekyll cruft

## Goal

Quarto renders exactly the intended inputs. Dead Jekyll files and the Marie Curie CV
template are removed from the repo. This unblocks a clean `quarto render` with no
spurious pages in `_site/`.

## Problem

`_quarto.yml` has no `project: render:` list, so Quarto tries to build *everything* —
including `cv/cv.Rmd` (the stock Marie Curie vitae demo) and potentially anything
under `_includes/`. Also, many Jekyll-era files are still tracked in git even though
Quarto never uses them.

## Steps

- [x] In `_quarto.yml`, add a `project: render:` list using `*.qmd`, `*.md`,
  `!auto_cv.qmd` (excluded until frozen in task 04), `labnotes/**/*.qmd`,
  `courses/biolB215s19/*.Rmd`, `courses/biolB216s14/darwinAssembly.Rmd`.

- [x] **Remove the `cv/` directory entirely** — done via `git rm -r cv/`.

- [x] Remove Jekyll-only leftovers: `_includes/`, `Gemfile`, `Rakefile`,
  `css/default.css`, `css/Rhandout.css`, `css/shapbio.css` — all removed via `git rm`.

- [x] Verified no remaining `.qmd`/`.yml` references the deleted files.

## Files changed

`_quarto.yml`, removed: `cv/`, `_includes/`, `Gemfile`, `Rakefile`,
`css/default.css`, `css/Rhandout.css`, `css/shapbio.css`

## Done when

- `quarto render` completes with no errors.
- `_site/` contains no Marie Curie page (`_site/cv/cv.html` absent).
- `git status` shows none of the deleted files.
- No broken CSS references remain.
