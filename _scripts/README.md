# Scripts

Helper scripts run by hand from the repository root.
None of them run as part of `quarto render`.

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

## Formatting

```bash
pixi run fmt    # ruff format + ruff check --fix on _scripts/
```
