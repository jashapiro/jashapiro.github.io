# Task 07 — Refresh papers.bib programmatically

> **Status (2026-10-24):** replanned. Now a Python script (`_scripts/sync_papers.py`,
> run via pixi) using ORCID's public API with no login, instead of an R script using
> `rorcid`/`rcrossref` with an OAuth token. Do this before task 04, which renders the
> CV publications from `papers.bib`.
> Done 2026-10-24: `pixi run sync-papers` added Liang 2026 (bioRxiv), Lee 2024,
> OpenPBTA 2023 and Hawkins 2026 (via `--doi`); the OpenPBTA and Liang preprints were
> then removed, leaving 16 entries.

## Goal

An on-demand script that adds any missing works from ORCID to `papers.bib`, so the
bibliography stays current without hand-writing BibTeX. Live network calls are
confined to this script; rendering the site never needs them. Existing entries are
never rewritten, because they carry hand curation (title casing, italics) that the
CV's NLM citation style depends on (see task 04).

## Current state

- `papers.bib`: 14 entries (13 `@ARTICLE` + 1 `@UNPUBLISHED`), Paperpile/Zotero-style
  keys (e.g. `Shapiro2007-of`). It is the source of truth for the CV bibliography.
- It is **behind** the hand-written `cv.qmd`, which also lists Hawkins 2026 (ScPCA,
  *Cell Genomics*), Lee 2024 (*Nature Communications*) and the published OpenPBTA
  (*Cell Genomics* 2023, doi:10.1016/j.xgen.2023.100340).
- `Shapiro2022-kj` is the OpenPBTA bioRxiv preprint (doi:10.1101/2022.09.13.507832).
- No `.httr-oauth` or `.Renviron` exists in the repo; the old plan's ORCID token is not
  available, and isn't needed for public reads.
- Python helper-script conventions are set by `_scripts/new_post.py`: pixi environment
  (`pixi.toml`), typer CLI, ruff, a `pixi run` task, a section in `_scripts/README.md`.

## Steps

- [x] Write `_scripts/sync_papers.py` (typer; `pixi run sync-papers`):
  1. Fetch work DOIs from `https://pub.orcid.org/v3.0/0000-0002-6224-0347/works`
     (JSON, no token).
  2. Read `papers.bib` as text; collect existing DOIs (case-insensitive) and
     normalized titles with a regex. No BibTeX parser, so existing entries are left
     byte-for-byte unchanged.
  3. For each ORCID DOI not already present, fetch BibTeX from `https://doi.org/<doi>`
     with `Accept: application/x-bibtex`. Give it a key in the owner's style,
     `<FirstAuthorFamily><Year>-<word>`: the script asks for the word for each new
     paper, suggesting the first title acronym or distinctive title word, and refuses
     keys already in use. (Claude Haiku and then Apple Intelligence's on-device model
     were tried for choosing the word and dropped on 2026-10-24: the local model picked
     poor words such as "anndata" for ScPCA.)
  4. Append new entries to `papers.bib`; print what was added, or "nothing new".
  5. `--dry-run` prints what would be added without writing.
  - As built: entries are built from Crossref's JSON (not its one-line BibTeX), in
    the file's Paperpile layout; `--doi` adds DOIs not on ORCID; DOIs in the
    `[[skip]]` tables of `papers-sync.toml` (repo root) are ignored.
- [x] Preprints: for each `@UNPUBLISHED` (or bioRxiv-DOI) entry, check Crossref
  (`https://api.crossref.org/works/<doi>`, `relation.is-preprint-of`) for a published
  version. Print a flag naming both DOIs; don't edit or delete the preprint entry. If
  the published DOI is missing, it's appended by the normal path.
- [x] Crossref "polite pool": if `CROSSREF_EMAIL` is set in the environment, send it
  as `mailto`; otherwise send nothing. Never hard-code an address.
- [x] Add the `sync-papers` task to `pixi.toml` (no new dependencies expected; stdlib
  `urllib`/`json` plus typer).
- [x] Document in `_scripts/README.md`, including the post-run curation checklist:
  - Protect proper nouns in titles with braces and italicize taxa with `\textit{}`
    (NLM applies sentence case; see task 04).
  - Use the full author name form `Shapiro, Joshua A` (the bolding filter matches it).
  - Add new equal-contribution papers to the CV's front-matter list (task 04).
- [x] Run it once (needs `pub.orcid.org`, `doi.org` and `api.crossref.org` allowed
  through the sandbox firewall) and confirm the three missing papers are added.
  - ORCID has ScPCA only as the 2024 bioRxiv preprint, and Crossref doesn't link it to
    the 2026 *Cell Genomics* article, so the article was added with `--doi` and the
    preprint DOI is listed under `[[skip]]` in `papers-sync.toml`. The owner
    then added the article to ORCID (2026-10-24), so `--doi` is no longer needed; ORCID
    still lists the preprint separately, so it stays in the skip file.
  - ORCID also had a 2026 preprint not in the old CV (Liang et al., bioRxiv). The owner
    doesn't want it on the CV for now, so it was removed and its DOI added to the skip file;
    delete that line and re-run to add it later.
  - `Shapiro2022-kj` (OpenPBTA preprint) was reported as published and removed at the
    owner's request; the published `Shapiro2023-op` replaces it.

## Files changed

New: `_scripts/sync_papers.py`, `papers-sync.toml`; updated: `pixi.toml`, `pixi.lock` (if the task list
changes it), `_scripts/README.md`, `papers.bib` (on each run).

## Done when

- `pixi run sync-papers` runs without error and either appends new entries to
  `papers.bib` or reports "nothing new"; `--dry-run` writes nothing.
- Existing entries are untouched (`git diff papers.bib` shows only additions).
- The OpenPBTA preprint is flagged as published.
