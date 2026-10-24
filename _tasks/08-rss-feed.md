# Task 08 — RSS feed for lab notes

## Goal

A discoverable, valid RSS feed of `labnotes/` posts that readers can subscribe to
from anywhere on the site, and that old Jekyll-era feed subscribers can still reach.

## Current state

- `labnotes.qmd` already has a `listing.feed` block (title "ShapBio Lab Notes"), so
  Quarto generates `_site/labnotes.xml` (RSS 2.0) with one `<item>` per post, using
  `website.site-url` (`https://shapbio.me/`) for absolute links. Live URL:
  `https://shapbio.me/labnotes.xml`.
- Items currently carry **full post content** in `<description>` (Quarto's default
  `type: full`), including margin/footnote markup.
- The `<link rel="alternate" type="application/rss+xml">` autodiscovery tag is only
  emitted on `labnotes.html` — not on the home page or on individual posts.
- No visible RSS link/icon anywhere on the site.
- `<dc:creator>` renders as `Josh ` (trailing space) from `author: "Josh"`.
- The old Jekyll site published `atom.xml` at the site root (`source/atom.xml` /
  `source/atom.haml` in git history); any old subscribers point there and now get a 404.
- Newest post is dated `2027-10-04` (likely a typo for 2026), which makes the feed's
  `<lastBuildDate>` a future date — fix separately, but check the feed after.

## Steps

- [ ] Decide full vs. summary items. Options: keep `type: full` (readers see whole
  post), or set `feed: { type: partial }` so items use the `description` field plus
  a link. Check how margin notes/footnotes render in a real reader (e.g. NetNewsWire)
  before deciding.

- [ ] Add a visible feed link: e.g. a `navbar.right` entry with
  `icon: rss` and `href: labnotes.xml` in `_quarto.yml`, and/or a line in
  `labnotes.qmd`'s subtitle area.

- [ ] Site-wide autodiscovery: add the alternate link to every page via
  `format.html.include-in-header` in `_quarto.yml`:
  ```html
  <link rel="alternate" type="application/rss+xml" title="ShapBio Lab Notes"
        href="https://shapbio.me/labnotes.xml">
  ```
  Use an absolute href so it resolves from post subdirectories. Confirm it doesn't
  duplicate the tag Quarto already emits on `labnotes.html` (if it does, either accept
  the duplicate or scope the include to non-listing pages).

- [ ] Legacy `atom.xml`: GitHub Pages can't do server-side redirects. Options:
  (a) accept the break — probably fine given how old the Jekyll feed is; or
  (b) add a render step / resource that copies `labnotes.xml` to `atom.xml` (most
  readers accept RSS at any URL regardless of the filename). Choose and document.

- [ ] Optional: per-category feeds via `feed: { categories: [...] }` (Quarto generates
  `labnotes-<category>.xml`). Only worth it if categories get real use.

- [ ] Fix the `dc:creator` trailing space if it bothers anyone — e.g. use the
  structured form `author: { name: "Josh Shapiro" }` in posts / `labnotes/_metadata.yml`.
  Coordinate with task 06's front-matter template.

- [ ] Validate: run the rendered feed through https://validator.w3.org/feed/ (after
  deploy) and subscribe in a real reader. Confirm `draft: true` posts are excluded.

## Files changed

`_quarto.yml` (navbar, header include), `labnotes.qmd` (feed options), possibly
a small header include file, `labnotes/_metadata.yml` (author), and the task 06
template if the author field changes.

## Done when

- `https://shapbio.me/labnotes.xml` validates with no errors.
- Browsers / feed readers auto-discover the feed from the home page and from any post.
- There is a visible RSS link on the site.
- Draft posts don't appear in the feed.
- The `atom.xml` decision is made and documented.
