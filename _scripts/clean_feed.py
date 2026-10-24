"""Clean up the lab notes RSS feed.

Run by Quarto as a project post-render script (see `_quarto.yml`), so it uses
only the standard library: CI runs it with the system python3, not pixi.
Removes every margin container (footnotes and asides rendered in the margin)
from the feed item content, along with the in-text footnote markers that
pointed to them, and makes relative links absolute (Quarto only does this for
images). The rendered site pages are not touched.
"""

import os
import re
from pathlib import Path
from urllib.parse import urljoin

FEED = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site")) / "labnotes.xml"

MARGIN_DIV = re.compile(r'<div class="[^"]*\bcolumn-margin\b[^"]*"[^>]*>')
DIV_TAG = re.compile(r"<(/?)div\b[^>]*>")
FOOTNOTE_ID = re.compile(r'id="fn(\d+)"')
ITEM = re.compile(r"<item>.*?</item>", re.DOTALL)
ITEM_LINK = re.compile(r"<link>(.*?)</link>")
DESCRIPTION = re.compile(
    r"(<description><!\[CDATA\[)(.*?)(\]\]></description>)", re.DOTALL
)
URL_ATTR = re.compile(r'\b(href|src)="([^"#][^"]*)"')


def remove_margin_divs(html: str) -> tuple[str, set[str]]:
    """Remove margin divs (with their nested divs); return the footnote numbers they held."""
    footnotes = set()
    while match := MARGIN_DIV.search(html):
        depth = 0
        for tag in DIV_TAG.finditer(html, match.start()):
            depth += -1 if tag.group(1) else 1
            if depth == 0:
                break
        else:
            raise ValueError("unbalanced <div> in feed item")
        footnotes.update(FOOTNOTE_ID.findall(html, match.start(), tag.end()))
        html = html[: match.start()] + html[tag.end() :]
    return html, footnotes


def clean_html(html: str, base: str) -> str:
    html, footnotes = remove_margin_divs(html)
    # Quarto's feed already unwrapped the footnote links, leaving bare <sup>N</sup>
    for number in footnotes:
        html = re.sub(rf"<sup>{number}</sup>", "", html)
    # resolve relative links against the post's URL; absolute ones are unchanged
    return URL_ATTR.sub(lambda m: f'{m.group(1)}="{urljoin(base, m.group(2))}"', html)


def clean_item(match: re.Match) -> str:
    item = match.group(0)
    base = ITEM_LINK.search(item).group(1)
    return DESCRIPTION.sub(
        lambda m: m.group(1) + clean_html(m.group(2), base) + m.group(3), item
    )


def main() -> None:
    # the feed is only written on a full project render
    if not FEED.exists():
        return
    text = FEED.read_text(encoding="utf-8")
    cleaned = ITEM.sub(clean_item, text)
    if cleaned != text:
        FEED.write_text(cleaned, encoding="utf-8")


if __name__ == "__main__":
    main()
