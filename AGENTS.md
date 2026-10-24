# AGENTS.md

This file provides guidance to Claude Code (claude.ai/code) and other agents when working with code in this repository.

## What this is

Personal website for Joshua A. Shapiro (shapbio.me), built with Quarto.
It is mid-migration from a Jekyll/Rmarkdown site — the `master` branch holds the old Jekyll site; all active work is on the `quarto` branch.

## Formatting

- **Text** (`.qmd`, `.md`): one sentence per line.
- **R code**: format with `air` (default settings).
- **Python code**: format with `ruff` (default settings).
- **File names**: kebab-case. Use underscores only to separate distinct, machine-parseable chunks, such as the date and slug in `labnotes/2026-10-04_two-more-years/`. Python scripts keep snake_case (e.g. `_scripts/new_post.py`).

## Key constraint: never write site content

Do not write prose that will appear on the published site.
Fixing spelling or grammar errors is fine.
Reformatting existing text (e.g., one-sentence-per-line) is fine.
Copying text verbatim from a source the owner has provided is fine.
Generating original prose for pages, blog posts, the CV, or any other published content is not permitted under any circumstances.

## Key constraint: no git commands

Do not run any git commands that modify the repository (commit, add, rm, checkout, reset, stash, branch, merge, rebase, push, etc.).
The owner handles all git operations.
Read-only commands (`git show`, `git log`, `git diff`, `git status`, `git blame`) are allowed, e.g. to recover content from history.

## Build commands

```bash
pixi run render       # quarto render: full build → _site/
pixi run preview      # quarto preview: live-reloading dev server
pixi run new-post     # scaffold a new labnotes post (see _scripts/README.md)
pixi run sync-papers  # add missing ORCID works to papers.bib
pixi run fmt          # ruff format + check for Python in _scripts/
```

Quarto, Python, and Python tooling come from the pixi environment (`pixi.toml`, locked by `pixi.lock`).
R and R package dependencies are managed separately via `renv`.

## Architecture

### Render scope

`_quarto.yml` has an explicit `render:` list (root pages, labnotes posts, and the one remaining course).

### Freeze

Computational R outputs are frozen so the site renders without re-executing R:
- `_freeze/courses/` — frozen course tutorial outputs (committed; render without R).
- `_freeze/labnotes/` — frozen blog post session-info outputs.

`_freeze/` is committed to the repo (not gitignored).
`_site/` is gitignored.

### Styling

These CSS/SCSS files are wired into the build:
- Site fonts are self-hosted (no font CDN): Source Sans 3 and Source Code Pro `.woff2` subsets in `fonts/*/web/`, declared in `css/fonts.scss` (first in the theme list); Quarto copies them next to the compiled CSS, and `_quarto.yml` publishes their `LICENSE.txt` files. The CV PDF uses Source Sans 3 from the `.otf` files in `fonts/source-sans-3/`. See the README in each `fonts/` folder.
- `css/shapbio.scss` — site-wide theme overlay on top of Bootstrap `litera`. Contains `figure.boxed`, `.pull-left/.pull-right`, `.file-link`, `.subhead` (pulls a line up under the preceding heading; pair with Bootstrap `.text-end` to right-align).
- `css/cv.css` — old CV list styles (unbulleted lists, `.self`, `.species`, ...). Still referenced from `cv.qmd` front matter; task 05 removes it.

### CV

`cv.qmd` renders to the HTML CV page and to `cv.pdf` (Typst), which Quarto links from the page under "Other Formats". No R and no network access are needed.
- Research Interests, Experience, Education and Honors are hand-written markdown in `cv.qmd`.
- Publications are every entry in `papers.bib` (`nocite: "@*"`; 16 entries; `pixi run sync-papers` adds new ORCID works), formatted by `cv.csl`: the CSL project's NLM name-year style, modified to sort newest first (up to 6 authors, then "et al.").
- The PDF layout is in `_typst/cv/`: Quarto template partials that define a `cv` function (`typst-template.typ`) and call it in place of the default `article` (`typst-show.typ`). Partials must keep Quarto's file names, so other Typst layouts get their own folder. Layout: section headings in the left margin, Source Sans 3 (from `fonts/source-sans-3/` via `font-paths`, so local and CI builds match), hanging indents instead of bullets, name and page number in the header after page 1.
- `_scripts/copy_cv_pdf.py` (post-render) also publishes the PDF at `docs/JAShapiro_CV.pdf`, the old CV's address; that file isn't committed.
- `_filters/cv-publications.lua` runs citeproc itself (Quarto otherwise runs it after all filters), then bolds the `highlight-author` name and adds `*` to the names listed per citation key in `equal-contribution` (both in `cv.qmd` front matter).
- Pandoc puts English BibTeX titles in sentence case, so `papers.bib` titles brace proper nouns (`{OpenPBTA}`) and wrap taxa as `{\textit{Drosophila}}`. Author names stay as published; `highlight-author` lists each form of the owner's name.

### Blog (labnotes)

Posts live at `labnotes/<YYYY-MM-DD>_<slug>/index.qmd`.
Shared session-info block is in `labnotes/_sessioninfo.qmd` — include it with `{{< include ../_sessioninfo.qmd >}}`.
Per-post `freeze: true` and `date-format: iso` are inherited from `labnotes/_metadata.yml`.

### Courses

Only one course dir still has renderable content:
- `courses/biolB215s19/` — 12 tutorial `.qmd` files (converted from Jekyll-era `.Rmd`) + `index.qmd`.

The `f14/f15/s13/s14/s18` course dirs contain only syllabus PDFs — their tutorial pages were intentionally removed and those old deep links are accepted 404s.

## Task tracking

Remaining work is tracked as markdown files in `_tasks/` (the `_` prefix prevents Quarto from publishing the directory).
Each file has a checklist of steps and a "done when" criterion.
Current tasks:

| File | Topic |
|---|---|
| `02-courses-url-preservation.md` | Convert `biolB215s19/index.markdown` → `.qmd`; remove unfinished `biolB216s14` |
| `03-frontmatter-and-404.md` | Strip stale Jekyll front matter; add `404.qmd` |
| `04-cv-auto-build.md` | Built: `cv.qmd` on Quarto citations (NLM `cv.csl`, `_filters/cv-publications.lua`) with a Typst PDF; open: et al. cases, PDF layout, old `docs/` PDF, `renv::snapshot()` |
| `05-cv-and-site-styling.md` | Retire `css/cv.css`; any CV tweaks go in `css/shapbio.scss` (after 04) |
| `06-new-post-script.md` | Done: `_scripts/new_post.py` (`pixi run new-post`); remaining: commit `pixi.lock`, check in preview |
| `07-papers-bib-sync-script.md` | Done: `_scripts/sync_papers.py` (`pixi run sync-papers`) adds missing ORCID works to `papers.bib` |
| `08-rss-feed.md` | Done: feed cleanup via `_scripts/clean_feed.py`, RSS icons, autodiscovery; remaining: check in a real feed reader |
