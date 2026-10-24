# Task 04 — Rebuild the CV on Quarto citations (HTML + PDF)

> **Status (2026-10-24):** replanned. Dropped the `vitae`/`rorcid` approach in
> `auto_cv.qmd` (live ORCID call at render, needed freezing). The CV is now `cv.qmd`
> rendered by Quarto alone: publications from `papers.bib` via citeproc with an
> NLM style, everything else hand-written markdown, plus a Typst PDF offered as a
> download link. No R involved. Do task 07 first so `papers.bib` is complete.
>
> **Built 2026-10-24** (all steps below); remaining: the open decisions, the owner's
> visual check, and `renv::snapshot()` on the Mac to drop `vitae`/`rorcid`/`rcrossref`.

## Goal

One `cv.qmd` that renders to the site's HTML CV page (`cv.html`, same URL and navbar
entry as now) and to a PDF via Typst, linked from the page for download only. Built
entirely from files in the repo, so CI renders it with no network calls or freezing.

## Current state

- `cv.qmd`: hand-written CV (Experience, Education, 16 publications as raw
  `<ul>/<li class="pub">` HTML with `[...]{.self/.species/.journal/.issue/.pages}`
  spans, Honors & Awards); styled by `css/cv.css`. It has a couple of broken
  publication entries (e.g. Dang 2021 markup). No Presentations section exists
  despite the old plan saying there were 10.
- `auto_cv.qmd`: `vitae::bibliography_entries("papers.bib")` plus unused ORCID
  fetches; excluded from the render list in `_quarto.yml`.
- `docs/JAShapiro_CV.pdf`: an old CV PDF, still published via `resources:
  docs/*.pdf` but not linked from any page.
- Quarto 1.9 ships Typst, so `quarto-dev/quarto-actions/setup` in CI already has it.

## Design decisions (settled 2026-10-24)

- **Citation style: NLM**, from the CSL repository's `nlm-name-year.csl`; up to 6
  authors, then "et al." (the style's default `et-al-min="7" et-al-use-first="6"`).
- **Newest first**: keep a modified copy as `cv.csl` whose bibliography `<sort>` is
  `issued` descending. Keep the CC BY-SA attribution; change `<title>` and `<id>`,
  and note the modification.
- **PDF is a download link only** (Quarto's automatic "Other formats" link from
  `format-links`). The HTML page stays the main CV.
- **Equal authorship**: `*` after the name in those entries, plus the existing
  "*Equal authorship contribution*" footnote line under the list.
- **Experience / Education / Honors stay hand-written**: ORCID lacks advisors,
  dissertation titles and grouped titles, so it isn't a source for these.

## Open decisions

- Entry tail: NLM default ends entries with `doi:…` and `PubMed PMID: …`; alternatively
  drop the PMID and make the DOI a link.
- Authors hidden by "et al.": NLM shows 6 authors, so the owner's name doesn't appear
  for Dang 2021 (16th author) or Guo 2020 (9th). The old CV hid Dang too but listed
  all of Guo's authors.
- `docs/JAShapiro_CV.pdf`: decided 2026-10-24: the committed old PDF is removed, and
  the post-render script `_scripts/copy_cv_pdf.py` copies the built `cv.pdf` to
  that address in `_site`, so old links get the current CV.
- Typst PDF layout: done 2026-10-24 in `_typst/cv/typst-template.typ`, modeled on
  `docs/JAShapiro_CV.pdf` (margin headings, blue accent, hanging indents, running
  header). Font: Source Sans 3 from `fonts/source-sans-3/`, matching the site's
  Source Sans (Helvetica Neue can't be committed and CI doesn't have it).

## Steps

- [x] **Curate `papers.bib`** (after task 07 adds the missing papers) so it renders
  correctly in NLM sentence case: brace proper nouns and acronyms in titles
  (`{OpenPBTA}`, `{X}-linked`, `{Bryn Mawr}`), wrap taxa as `{\textit{Drosophila}}`,
  and use `Shapiro, Joshua A` for every author entry (Kohn 2008 and Lee 2005 have
  `Shapiro, J`). Check each entry against the current `cv.qmd` list.
  - Author names stay as published (owner's request): Kohn 2008 and Lee 2005 keep
    `Shapiro, Joshua`, and `highlight-author` lists both `Shapiro JA` and `Shapiro J`.
    Title braces/`{\textit{}}` are kept. (Reading the bib under a non-English `lang`
    to skip pandoc's sentence-casing also worked, but the owner preferred braces.)
- [x] **Add `cv.csl`** (modified `nlm-name-year.csl`, see above).
- [x] **Lua filter: bold own name.** `_filters/cv-self.lua` (or similar) wraps
  `Shapiro JA` inside the bibliography (`#refs` / `.csl-entry`) in `Strong`, so it
  works in both HTML and Typst.
- [x] **Lua filter: equal contribution.** Front-matter list, e.g.
  `equal-contribution: [Andersen2012-ag, Schacherer2009-jp, Lu2010-fk]`; the filter
  appends `*` after the bolded name in `#ref-<key>` entries. Keep the footnote line
  (verbatim from the current CV) after the `#refs` div.
  - As built: one filter, `_filters/cv-publications.lua`. Quarto runs citeproc after
    every user filter stage, so the filter calls `pandoc.utils.citeproc` itself and
    then clears `bibliography`/`nocite`. `highlight-author: Shapiro JA` and
    `equal-contribution` (a map of citation key to the co-first author names, e.g.
    `Andersen2012-ss: [Andersen EC, Gerke JP, Shapiro JA]`, matching the old CV's
    asterisks) are in `cv.qmd` front matter. No `citeproc: true` needed for Typst.
- [x] **Rewrite `cv.qmd` structure**:
  - Front matter: `bibliography: papers.bib`, `csl: cv.csl`, `nocite: "@*"`,
    `filters:`, and `format: { html: default, typst: { papersize: us-letter } }`
    with `citeproc: true` for Typst, so both outputs use the same CSL formatting
    rather than Typst's native bibliography.
  - Publications section: just a `::: {#refs}` div.
  - Experience, Education, Honors: keep the text verbatim, converting the raw
    HTML lists to markdown lists and `[...]{.species}` spans to `*...*`, so they render
    in Typst as well. (Reformatting only; no new prose.)
- [x] **Remove the old pieces**: delete `auto_cv.qmd`; remove `"!auto_cv.qmd"` from the
  `_quarto.yml` render list; drop `vitae`, `rorcid` and `rcrossref` from
  `dependencies.R` and `renv.lock` (`renv::snapshot()` on the Mac) if nothing else
  uses them.
  - Deleted `auto_cv.qmd` and `dependencies.R` (it only held `library(rcrossref)`).
    `renv.lock` still lists the packages until `renv::snapshot()` runs on the Mac.
- [x] **Check both outputs**: HTML matches the site theme and has the PDF link; the PDF
  is readable on letter paper; publication list matches the old hand-written list.
  - Checked in a sandbox render: 16 entries, newest first, name bold in 14 (not the two
    "et al." cases), `*` on the three co-first papers, PDF 4 letter pages with an
    "Other Formats" link from the HTML. Owner's visual check still to do.
- [x] Update `AGENTS.md` (CV section) to describe the new setup.

## Files changed

`cv.qmd`, `papers.bib`, new `cv.csl`, new Lua filter(s), `_quarto.yml`, deleted
`auto_cv.qmd`, `dependencies.R`/`renv.lock`, `AGENTS.md`; possibly `docs/JAShapiro_CV.pdf`.

## Done when

- `cv.html` shows Experience, Education, Publications (from `papers.bib`, NLM, newest
  first, own name bold) and Honors, with a working PDF download link.
- `quarto render` in CI produces both with no network access and no `_freeze` entry.
- `auto_cv.qmd` and the `vitae`/`rorcid` dependencies are gone.
