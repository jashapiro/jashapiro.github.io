# Task 07 — Refresh papers.bib programmatically

## Goal

An on-demand R script that pulls works from ORCID / Crossref and updates `papers.bib`,
so the bibliography stays current without hand-editing BibTeX. Live network/auth calls
are intentionally confined to this script; rendering the CV never needs them.

## Current state

- `papers.bib` is a committed 14-entry BibTeX file (13 `@ARTICLE` + 1 `@UNPUBLISHED`),
  keys in Zotero/Better-BibTeX style (e.g. `Shapiro2007-of`). It is the source of
  truth for the CV bibliography.
- `dependencies.R` records `library(rcrossref)` — Crossref is preferred for BibTeX
  retrieval (ORCID's own citation export is less well-formatted).
- `rorcid` is already used in `auto_cv.qmd` for ORCID API access.
- `.Renviron` (gitignored) can hold `CROSSREF_EMAIL=...` and the ORCID token path.
  `.httr-oauth` (gitignored) caches the ORCID OAuth token.

## Steps

- [ ] Write `_scripts/sync_papers.R`. Invocation:
  ```
  Rscript _scripts/sync_papers.R
  ```
  Recommended approach:
  1. Pull the list of work DOIs from ORCID: `rorcid::orcid_works("0000-0002-6224-0347")`
     → extract DOIs.
  2. For each DOI, fetch a BibTeX entry via `rcrossref::cr_cn(dois, format = "bibtex")`.
  3. Load the existing `papers.bib` (e.g. with `bib2df` or a simple regex parse, or
     just track existing keys by scanning `@ARTICLE{<key>,`).
  4. For each fetched entry, check if a matching entry already exists (match on DOI
     field or title). If it does and the existing entry has hand-edits (e.g.
     `abstract`, custom notes), preserve it (don't overwrite). If new, append.
  5. Write `papers.bib` back, committing the changes by hand afterward.
  - Consider a `--dry-run` flag that prints what would be added/changed without
    writing.

- [ ] Handle the `@UNPUBLISHED` entry (`Shapiro2022-kj`, the OpenPBTA atlas) — likely
  it now has a DOI/published version. The script should detect it is now published
  (DOI resolves) and offer to upgrade the entry type, or at least flag it.

- [ ] Document in `_scripts/README.md` (task 06 creates this file; add a section here).

- [ ] Update `renv.lock` if new packages are added (`renv::snapshot()`).

## Required credentials (local only)

- `CROSSREF_EMAIL` in `.Renviron` (polite pool for Crossref — recommended).
- `.httr-oauth` for ORCID OAuth (already in place from `auto_cv.qmd` development).

## Files changed

New: `_scripts/sync_papers.R`; updated: `_scripts/README.md`, possibly `renv.lock`,
and `papers.bib` (on each run)

## Done when

- `Rscript _scripts/sync_papers.R` runs without error and either appends new entries
  to `papers.bib` or reports "nothing new".
- Existing entries with hand-curation are not clobbered.
- The `@UNPUBLISHED` preprint status is handled (flagged or updated).
- After running, `quarto render` picks up any new bib entries in the CV bibliography.
