# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Personal website for Joshua A. Shapiro (shapbio.me), built with Quarto. It is mid-migration from a Jekyll/Rmarkdown site — the `master` branch holds the old Jekyll site; all active work is on the `quarto` branch.

## Formatting

- **Text** (`.qmd`, `.md`): one sentence per line.
- **R code**: format with `air` (default settings).
- **Python code**: format with `ruff` (default settings).

## Key constraint: never write site content

Do not write prose that will appear on the published site.
Fixing spelling or grammar errors is fine.
Reformatting existing text (e.g. one-sentence-per-line) is fine.
Copying text verbatim from a source the owner has provided is fine.
Generating original prose for pages, blog posts, the CV, or any other published content is not permitted under any circumstances.

## Key constraint: no git commands

Do not run any git commands. The owner handles all git operations.

## Build commands

```bash
quarto render       # full build → _site/
quarto preview      # live-reloading dev server
```

R package dependencies are managed via `renv`.

## Architecture

### Render scope

`_quarto.yml` has an explicit `render:` list. Not everything in the tree is rendered:
- `auto_cv.qmd` is **excluded** from the render list (it requires a live ORCID API call via `.httr-oauth`; excluded until it is frozen — see `_tasks/04-cv-auto-build.md`).
- `courses/biolB215s19/index.markdown` is a Jekyll file — **not rendered** by Quarto (task 02 will convert it to `index.qmd`).
- `error.markdown` is a Jekyll 404 — **not rendered** (task 03 will replace it with `404.qmd`).

### Freeze

Computational R outputs are frozen so the site renders without re-executing R:
- `_freeze/courses/` — frozen course tutorial outputs (committed; render without R).
- `_freeze/labnotes/` — frozen blog post session-info outputs.
- `auto_cv.qmd` has **no freeze yet** — that's why it's excluded from the render list.

`_freeze/` is committed to the repo (not gitignored). `_site/` is gitignored.

### Styling

Two CSS/SCSS files are wired into the build:
- `css/shapbio.scss` — site-wide theme overlay on top of Bootstrap `litera`. Contains `figure.boxed`, `.pull-left/.pull-right`, `.file-link`.
- `css/cv.css` — CV-specific span styles (`.self`, `.species`, `.journal`, `.issue`, `.pub`). Referenced from `cv.qmd` front matter. Task 05 will fold this into `shapbio.scss` and remove it.

### CV

Two CV files coexist:
- `cv.qmd` — hand-written HTML CV; currently linked in the navbar. Source of truth for content today.
- `auto_cv.qmd` — ORCID + vitae-based auto CV (work in progress, excluded from render). When complete it will replace `cv.qmd` in the navbar.

Publications are driven by `papers.bib` (14 BibTeX entries). `auto_cv.qmd` uses `vitae::bibliography_entries("papers.bib", "Publications")` — no live Crossref/ORCID call needed for the bibliography itself.

### Blog (labnotes)

Posts live at `labnotes/<YYYY-MM-DD>_<slug>/index.qmd`. Shared session-info block is in `labnotes/_sessioninfo.qmd` — include it with `{{< include ../_sessioninfo.qmd >}}`. Per-post `freeze: true` and `date-format: iso` are inherited from `labnotes/_metadata.yml`.

### Courses

Only two course dirs still have renderable content:
- `courses/biolB215s19/` — 10 tutorial `.Rmd` files + `index.markdown` (Jekyll, needs conversion to `.qmd`).
- `courses/biolB216s14/` — `darwinAssembly.Rmd` only; no index yet.

The `f14/f15/s13/s14/s18` course dirs contain only syllabus PDFs — their tutorial pages were intentionally removed and those old deep links are accepted 404s.

## Task tracking

Remaining work is tracked as markdown files in `_tasks/` (the `_` prefix prevents Quarto from publishing the directory). Each file has a checklist of steps and a "done when" criterion. Current tasks:

| File | Topic |
|---|---|
| `02-courses-url-preservation.md` | Convert `biolB215s19/index.markdown` → `.qmd`; add `biolB216s14/index.qmd` |
| `03-frontmatter-and-404.md` | Strip stale Jekyll front matter; add `404.qmd` |
| `04-cv-auto-build.md` | Complete `auto_cv.qmd` (render edu/employment, freeze, wire into navbar) |
| `05-cv-and-site-styling.md` | Fold `css/cv.css` into `css/shapbio.scss`; remove standalone file |
| `06-new-post-script.md` | Write `_scripts/new_post.R` to scaffold new blog posts |
| `07-papers-bib-sync-script.md` | Write `_scripts/sync_papers.R` to refresh `papers.bib` from ORCID/Crossref |
