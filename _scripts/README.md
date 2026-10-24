# Scripts

Helper scripts run by hand from the repository root, except `clean_feed.py`, which Quarto runs after every full render.

Python scripts run in the [pixi](https://pixi.sh) environment defined in `pixi.toml` at the repository root (Python 3.14, typer, ruff, and Quarto).
`pixi run <task>` installs the environment on first use; `pixi.lock` pins it.
Run `pixi task list` to see the available tasks.

## `new_post.py`

Creates a draft lab notes post at `labnotes/<date>_<slug>/index.qmd`.

```bash
pixi run new-post                         # prompts for everything
pixi run new-post "My Title"              # prompts for the rest
pixi run new-post "My Title" --date 2025-06-01 --slug short-name -d "Description" -c R -c meta
pixi run new-post "My Title" --no-input   # no prompts: today, slug from title
pixi run new-post --help
```

Anything not given on the command line is prompted for (date defaults to today, slug to one made from the title), and the front matter is shown for confirmation before the post is written.
When not run in a terminal, or with `--no-input`, it uses the defaults without prompting.

The new post has `draft: true`, the `order: -YYYYMMDD` field used for newest-first sidebar sorting, and the session info include at the end.
The script refuses to overwrite an existing post directory.

pixi's task runner can't pass a straight apostrophe (`'`) in a command-line argument (it fails with "Expected closing single quote").
For a title like `Josh's Post`, either enter it at the prompt or bypass the task:

```bash
pixi run python _scripts/new_post.py "Josh's Post"
```

Remove `draft: true` when the post is ready to publish.

## `clean_feed.py`

Removes margin notes (and the footnote markers pointing to them) from the lab notes RSS feed, `_site/labnotes.xml`.
It is a project `post-render` script in `_quarto.yml`, so it runs automatically on `quarto render`; the rendered pages keep their margin notes.
It uses only the standard library because CI runs it with the runner's system `python3`, not the pixi environment.

## `sync_papers.py`

Adds works from the public ORCID record (`0000-0002-6224-0347`) that are missing from `papers.bib`, using Crossref metadata.
No ORCID login is needed.

```bash
pixi run sync-papers --dry-run                        # show what would be added
pixi run sync-papers                                  # append new entries, asking for each key
pixi run sync-papers --doi 10.1016/j.xgen.2026.101283 # also add a DOI not on ORCID
```

Entries already in `papers.bib` (matched by DOI) are never changed; new ones are appended in the file's existing layout.
For each new paper the script shows the title and DOI and asks for the word in its key, `<Family><Year>-<word>` (e.g. `Hawkins2026-scpca`).
Press Enter to accept the suggestion: the first acronym of a capitalized name in the title (`scpca` for "Single-Cell Pediatric Cancer Atlas"), otherwise the first distinctive title word.
With `--no-input`, with `--dry-run`, or when not run in a terminal, it uses the suggestions without asking.
A preprint that Crossref links to a published article is replaced by the article, and existing `@UNPUBLISHED` entries that have since been published are reported (not removed).
DOIs in the `[[skip]]` tables of `papers-sync.toml` are ignored, e.g. a preprint whose published version Crossref doesn't link, or a work left off the CV:

```toml
[[skip]]
doi = "10.64898/2026.09.14.750241"
reason = "Liang et al. 2026 preprint; left off the CV for now"
```
If `CROSSREF_EMAIL` is set, it is sent to Crossref to identify the script.

After a run, curate the new entries by hand:

- Brace proper nouns and acronyms in titles (`{OpenPBTA}`) and italicize taxa as `{\textit{Drosophila}}`; the CV's NLM style puts titles in sentence case.
- Check that author names use the full form `Shapiro, Joshua A`.
- Add equal-contribution papers to the CV's front-matter list (see `_tasks/04-cv-auto-build.md`).

## Formatting

```bash
pixi run fmt    # ruff format + ruff check --fix on _scripts/
```
