"""Create a new draft lab notes post.

Run with `pixi run new-post`; any values not given on the command line are
prompted for. Creates labnotes/<date>_<slug>/index.qmd with front matter
(including the `order` field used for newest-first sidebar sorting) and the
session info include.
"""

import datetime
import re
import sys
import unicodedata
from pathlib import Path
from typing import Annotated

import typer

ROOT = Path(__file__).resolve().parent.parent
LABNOTES_DIR = ROOT / "labnotes"
AUTHOR = "Josh S"

app = typer.Typer(add_completion=False)


def slugify(text: str) -> str:
    """Lowercase ASCII slug: apostrophes dropped, other non-alphanumerics -> '-'."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"['’]", "", text.lower())
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def yaml_quote(text: str) -> str:
    """Double-quote a string for YAML."""
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def parse_date(value: str) -> datetime.date:
    try:
        return datetime.date.fromisoformat(value)
    except ValueError:
        raise typer.BadParameter(f"invalid date {value!r}; use YYYY-MM-DD") from None


def parse_categories(value: str) -> list[str]:
    return [c.strip() for c in value.split(",") if c.strip()]


def post_dir(date: datetime.date, slug: str) -> Path:
    return LABNOTES_DIR / f"{date.isoformat()}_{slug}"


def check_slug(value: str, date: datetime.date) -> str:
    """Slugify `value` and make sure the post directory is free."""
    slug = slugify(value)
    if not slug:
        raise typer.BadParameter("slug must contain at least one letter or digit")
    if post_dir(date, slug).exists():
        raise typer.BadParameter(f"{post_dir(date, slug).relative_to(ROOT)} exists")
    return slug


def existing_categories() -> list[str]:
    """Categories used in existing posts' front matter."""
    found: set[str] = set()
    for qmd in LABNOTES_DIR.glob("*/index.qmd"):
        if not (
            front_matter := re.match(r"---\n(.*?\n)---", qmd.read_text(), re.DOTALL)
        ):
            continue
        if block := re.search(
            r"^categories:\n((?:\s+-.*\n)+)", front_matter[1], re.MULTILINE
        ):
            found.update(
                item.strip().strip("'\"")
                for item in re.findall(r"^\s+-\s*(.+)$", block[1], re.MULTILINE)
            )
    return sorted(found, key=str.casefold)


def render_post(
    title: str, description: str, date: datetime.date, categories: list[str]
) -> str:
    if categories:
        category_lines = "categories:\n" + "".join(
            f"  - {yaml_quote(c)}\n" for c in categories
        )
    else:
        category_lines = "categories: []\n"
    return (
        "---\n"
        f"title: {yaml_quote(title)}\n"
        f"description: {yaml_quote(description)}\n"
        f"author: {yaml_quote(AUTHOR)}\n"
        f'date: "{date.isoformat()}"\n'
        f"order: -{date:%Y%m%d}\n"
        f"{category_lines}"
        "draft: true\n"
        "---\n"
        "\n"
        "\n"
        "\n"
        "{{< include ../_sessioninfo.qmd >}}\n"
    )


@app.command()
def main(
    title: Annotated[
        str | None, typer.Argument(help="Post title.", show_default=False)
    ] = None,
    date: Annotated[
        datetime.date | None,
        typer.Option(
            "--date",
            parser=parse_date,
            metavar="YYYY-MM-DD",
            help="Post date (default: today).",
            show_default=False,
        ),
    ] = None,
    slug: Annotated[
        str | None,
        typer.Option(help="Directory slug (default: from title).", show_default=False),
    ] = None,
    description: Annotated[
        str | None,
        typer.Option("--description", "-d", help="One-line description."),
    ] = None,
    categories: Annotated[
        list[str] | None,
        typer.Option("--category", "-c", help="Category (repeatable)."),
    ] = None,
    no_input: Annotated[
        bool,
        typer.Option(
            "--no-input",
            help="Don't prompt; use defaults for anything not given. "
            "Implied when not run in a terminal.",
        ),
    ] = False,
) -> None:
    """Create a new draft post in labnotes/.

    Values not given as arguments are prompted for interactively.
    """
    interactive = not no_input and sys.stdin.isatty()
    today = datetime.datetime.now().astimezone().date()

    if title is None:
        if not interactive:
            raise typer.BadParameter("a title is required", param_hint="TITLE")
        title = typer.prompt("Title").strip()

    if date is None:
        date = (
            typer.prompt("Date", default=today.isoformat(), value_proc=parse_date)
            if interactive
            else today
        )

    if slug is not None:
        slug = check_slug(slug, date)
    elif interactive:
        slug = typer.prompt(
            "Slug",
            default=slugify(title),
            value_proc=lambda value: check_slug(value, date),
        )
    else:
        slug = check_slug(title, date)

    if description is None:
        description = (
            typer.prompt("Description", default="", show_default=False).strip()
            if interactive
            else ""
        )

    if categories is None:
        categories = []
        if interactive:
            if known := existing_categories():
                typer.secho(f"Existing categories: {', '.join(known)}", dim=True)
            categories = typer.prompt(
                "Categories (comma-separated)",
                default="",
                show_default=False,
                value_proc=parse_categories,
            )

    target = post_dir(date, slug) / "index.qmd"
    if interactive:
        typer.echo()
        typer.echo(render_post(title, description, date, categories))
        if not typer.confirm(f"Create {target.relative_to(ROOT)}?", default=True):
            raise typer.Abort()

    target.parent.mkdir(parents=True)
    target.write_text(render_post(title, description, date, categories))
    typer.secho(f"Created {target.relative_to(ROOT)}", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
