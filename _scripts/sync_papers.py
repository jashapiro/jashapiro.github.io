"""Add missing ORCID works to papers.bib.

Run with `pixi run sync-papers`. Reads the public ORCID record (no login), looks up
each DOI that papers.bib doesn't have yet in Crossref, and appends a new entry in the
file's existing layout. Existing entries are never rewritten, since they carry hand
curation (title casing, italics) the CV relies on.

Preprints that Crossref links to a published article are replaced by that article.
Existing @UNPUBLISHED entries are checked the same way and reported if published.
DOIs in the `[[skip]]` tables of papers-sync.toml are ignored (e.g. a preprint
Crossref doesn't link to its published version, or a work left off the CV).
Set CROSSREF_EMAIL to identify the script to Crossref's "polite pool".
"""

import html
import json
import os
import re
import textwrap
import tomllib
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Annotated

import typer

ROOT = Path(__file__).resolve().parent.parent
BIB = ROOT / "papers.bib"
CONFIG = ROOT / "papers-sync.toml"
ORCID_ID = "0000-0002-6224-0347"
ORCID_WORKS = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"
CROSSREF_WORKS = "https://api.crossref.org/works/"
MONTHS = [
    "jan",
    "feb",
    "mar",
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec",
]
# field values start in this column; continuation lines are indented to match
VALUE_COLUMN = 14
WIDTH = 79

app = typer.Typer(add_completion=False)


def normalize_doi(doi: str) -> str:
    doi = re.sub(
        r"^(https?://(dx\.)?doi\.org/|doi:)", "", doi.strip(), flags=re.IGNORECASE
    )
    return doi.lower()


def get_json(url: str) -> dict:
    headers = {"Accept": "application/json", "User-Agent": "shapbio-sync-papers"}
    if email := os.environ.get("CROSSREF_EMAIL"):
        headers["User-Agent"] += f" (mailto:{email})"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def orcid_dois() -> list[str]:
    """DOIs of the works on the ORCID record, one per work group."""
    dois = []
    for group in get_json(ORCID_WORKS)["group"]:
        for external_id in group["external-ids"]["external-id"]:
            if (
                external_id["external-id-type"] == "doi"
                and external_id["external-id-relationship"] == "self"
            ):
                dois.append(normalize_doi(external_id["external-id-value"]))
                break
    return dois


def crossref(doi: str) -> dict:
    return get_json(CROSSREF_WORKS + urllib.parse.quote(doi))["message"]


def published_doi(work: dict) -> str | None:
    """The DOI of the published article for a preprint, if Crossref knows it."""
    for relation in work.get("relation", {}).get("is-preprint-of", []):
        if relation.get("id-type") == "doi":
            return normalize_doi(relation["id"])
    return None


def is_preprint(work: dict) -> bool:
    return work.get("subtype") == "preprint"


def existing_entries(bib: str) -> tuple[set[str], set[str], dict[str, str]]:
    """Existing DOIs, citation keys, and DOIs of @UNPUBLISHED entries by key."""
    dois = {
        normalize_doi(d)
        for d in re.findall(r'^\s*doi\s*=\s*"([^"]+)"', bib, re.MULTILINE)
    }
    keys = set(re.findall(r"^@\w+\{([^,]+),", bib, re.MULTILINE))
    unpublished = {}
    for match in re.finditer(
        r"^@UNPUBLISHED\{([^,]+),(.*?)^\}",
        bib,
        re.MULTILINE | re.DOTALL | re.IGNORECASE,
    ):
        if doi := re.search(r'^\s*doi\s*=\s*"([^"]+)"', match.group(2), re.MULTILINE):
            unpublished[match.group(1)] = normalize_doi(doi.group(1))
    return dois, keys, unpublished


def skipped_dois() -> set[str]:
    """DOIs from the `[[skip]]` tables of the config file."""
    if not CONFIG.exists():
        return set()
    config = tomllib.loads(CONFIG.read_text(encoding="utf-8"))
    return {normalize_doi(entry["doi"]) for entry in config.get("skip", [])}


def bib_text(text: str) -> str:
    """Crossref title/name text as BibTeX: italics kept, other markup dropped."""
    text = re.sub(r"<(i|em)>(.*?)</\1>", r"\\textit{\2}", text, flags=re.DOTALL)
    text = html.unescape(re.sub(r"<[^>]+>", "", text))
    text = re.sub(r"([&%$#_])", r"\\\1", text)
    return re.sub(r"\s+", " ", text.replace('"', '{"}')).strip()


def author_name(author: dict) -> str:
    if "family" not in author:
        # consortium or group author
        return "{" + bib_text(author.get("name", "")) + "}"
    given = re.sub(r"\b([A-Z])\.", r"\1", author.get("given", "")).strip()
    family = bib_text(author["family"])
    return f"{family}, {bib_text(given)}" if given else family


def make_key(work: dict, keys: set[str]) -> str:
    """`<FirstAuthorFamily><Year>-<xx>`, as in the existing Paperpile-style keys."""
    authors = work.get("author") or [{}]
    family = authors[0].get("family") or authors[0].get("name") or "Anon"
    family = unicodedata.normalize("NFKD", family).encode("ascii", "ignore").decode()
    family = re.sub(r"[^A-Za-z]", "", family)
    stem = f"{family}{issued(work)[0]}"
    title = re.sub(r"[^a-z]", "", bib_text(work["title"][0]).lower()) + "zz"
    for i in range(len(title) - 1):
        key = f"{stem}-{title[i : i + 2]}"
        if key not in keys:
            return key
    raise ValueError(f"no free citation key for {stem}")


def issued(work: dict) -> list[int]:
    for field in ("published-print", "published-online", "issued", "posted"):
        if parts := work.get(field, {}).get("date-parts", [[]])[0]:
            return parts
    return [0]


def format_field(name: str, value: str, quote: bool = True) -> str:
    value = f'"{value}"' if quote else f" {value}"
    lead = f"  {name:<8} = "
    lines = textwrap.wrap(
        value,
        width=WIDTH,
        initial_indent=lead,
        subsequent_indent=" " * VALUE_COLUMN,
        break_long_words=False,
        break_on_hyphens=False,
    )
    return "\n".join(lines)


def make_entry(work: dict, key: str) -> str:
    preprint = is_preprint(work)
    date = issued(work)
    fields = [
        ("title", bib_text(work["title"][0]), True),
        ("author", " and ".join(author_name(a) for a in work.get("author", [])), True),
    ]
    if preprint:
        server = (work.get("institution") or [{}])[0].get("name") or work.get(
            "publisher"
        )
        fields.append(("journal", bib_text(server), True))
    else:
        journal = (work.get("short-container-title") or work.get("container-title"))[0]
        fields.append(("journal", bib_text(journal), True))
        if "volume" in work:
            fields.append(("volume", work["volume"], not work["volume"].isdigit()))
        if "issue" in work:
            fields.append(("number", work["issue"], not work["issue"].isdigit()))
        if pages := work.get("page") or work.get("article-number"):
            fields.append(("pages", pages.replace("-", "--"), True))
    if len(date) > 1:
        fields.append(("month", MONTHS[date[1] - 1], False))
    fields.append(("year", str(date[0]), False))
    if issn := work.get("ISSN"):
        fields.append(("issn", issn[0], True))
    fields.append(("doi", work["DOI"], True))
    body = ",\n".join(format_field(name, value, quote) for name, value, quote in fields)
    kind = "UNPUBLISHED" if preprint else "ARTICLE"
    return f"@{kind}{{{key},\n{body}\n}}\n"


@app.command()
def main(
    extra_dois: Annotated[
        list[str] | None,
        typer.Option(
            "--doi",
            help="Also add this DOI, e.g. a paper not on ORCID yet (repeatable).",
        ),
    ] = None,
    dry_run: Annotated[
        bool, typer.Option("--dry-run", help="Print new entries; don't write.")
    ] = False,
) -> None:
    """Append works from ORCID (and any --doi) that are missing from papers.bib."""
    bib = BIB.read_text(encoding="utf-8")
    have, keys, unpublished = existing_entries(bib)
    have |= skipped_dois()

    candidates = orcid_dois() + [normalize_doi(d) for d in extra_dois or []]
    new_entries = []
    seen = set()
    for doi in candidates:
        if doi in have or doi in seen:
            continue
        seen.add(doi)
        try:
            work = crossref(doi)
        except urllib.error.HTTPError as error:
            typer.secho(
                f"Skipped {doi}: Crossref returned {error.code}", fg=typer.colors.YELLOW
            )
            continue
        if is_preprint(work) and (published := published_doi(work)):
            if published in have or published in seen:
                typer.echo(f"Skipped preprint {doi}: published as {published}")
                continue
            typer.echo(f"Preprint {doi} is published as {published}; adding that")
            seen.add(published)
            work = crossref(published)
        key = make_key(work, keys)
        keys.add(key)
        new_entries.append(make_entry(work, key))
        typer.secho(f"New: {key} ({work['DOI']})", fg=typer.colors.GREEN)

    for key, doi in unpublished.items():
        try:
            published = published_doi(crossref(doi))
        except urllib.error.HTTPError:
            continue
        if published:
            status = (
                "in papers.bib" if published in have or published in seen else "missing"
            )
            typer.secho(
                f"Preprint {key} ({doi}) is published as {published} ({status}); "
                "consider removing the preprint entry",
                fg=typer.colors.YELLOW,
            )

    if not new_entries:
        typer.echo("Nothing new.")
        return
    if dry_run:
        typer.echo("\n" + "\n".join(new_entries))
        typer.echo(f"Dry run: {len(new_entries)} entries not written.")
        return
    BIB.write_text(bib.rstrip("\n") + "\n\n" + "\n".join(new_entries), encoding="utf-8")
    typer.echo(f"Added {len(new_entries)} entries to {BIB.relative_to(ROOT)}.")


if __name__ == "__main__":
    app()
