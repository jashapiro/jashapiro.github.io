# Task 03 — Small page cleanups and custom 404

## Goal

Remove stale Jekyll front matter from content pages and add a functioning Quarto
custom 404 page.

## Steps

- [ ] **`research.qmd`**: remove the stale `permalink: /research/index.html` and the
  now-redundant `format: html` lines from the YAML front matter. Quarto determines
  the output path from the file's location; `permalink` is a Jekyll concept that
  Quarto ignores (but it's visual clutter and could confuse future edits).

  Before:
  ```yaml
  ---
  title: Research
  permalink: /research/index.html
  format: html
  ---
  ```
  After:
  ```yaml
  ---
  title: Research
  ---
  ```

- [ ] **Replace `error.markdown` with `404.qmd`**. The current `error.markdown` uses
  Jekyll's `layout: default` and references `josh@shapbio.net` (the old email). A
  Quarto website's 404 page is named `404.qmd` (or `404.md`) at the project root.

  - Delete `error.markdown`.
  - Create `404.qmd` with a minimal, friendly message. Use the correct email/contact
    address (`shapbio.me` domain; check what the site footer uses — the footer has
    `http://shapbio.me` as the canonical URL).
  - Example front matter:
    ```yaml
    ---
    title: "Page not found"
    ---
    ```

- [ ] Note the **accepted `/people/` → `/about/` breakage**: the old site had a
  `/people/` page (sourced from `people.html`); the new navbar uses `about.qmd` at
  `/about/`. Old links to `/people/` will 404 with no redirect. This is accepted
  because deployment/redirects are out of scope.

## Files changed

`research.qmd`, deleted: `error.markdown`, new: `404.qmd`

## Done when

- `research.qmd` has no `permalink:` or `format:` front matter keys.
- `_site/404.html` exists and contains the custom message.
- `_site/error.html` is absent (or irrelevant).
- The contact address in `404.qmd` matches the rest of the site.
