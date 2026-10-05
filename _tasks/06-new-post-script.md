# Task 06 — Ruby-free new-post scaffolding

## Goal

An on-demand R script that creates a new, ready-to-edit blog post under `labnotes/`,
replacing the old `rake post` Ruby task. No Ruby, Make, or additional tooling needed —
R is already a managed project dependency via `renv`.

## Old behaviour (Rakefile `post` task)

- Usage: `rake post title="A Title" [date="2012-02-09"]`
- Slugified title (lowercase, spaces → `-`, strip non-word chars)
- Created `_posts/<YYYY-MM-DD>-<slug>.markdown` with Jekyll front matter
- Target was `_posts/` for Jekyll — does not match the new Quarto structure at all

## New structure (existing posts as reference)

Posts live at `labnotes/<YYYY-MM-DD>_<slug>/index.qmd`. Key front matter fields
(from `labnotes/2025-03-02_another-start/index.qmd` and the session-info post):
```yaml
---
title: "Post title"
description: "One-line description"
author: "Josh"
date: "YYYY-MM-DD"
categories:
  - category
draft: true
---
```
`freeze: true` and `date-format: iso` are inherited from `labnotes/_metadata.yml`.

Posts include `{{< include ../_sessioninfo.qmd >}}` at the end (via the shared
session-info include introduced in the recent commits).

## Steps

- [ ] Create `_scripts/` directory in the repo root.

- [ ] Write `_scripts/new_post.R`. Invocation:
  ```
  Rscript _scripts/new_post.R "Post Title" [YYYY-MM-DD]
  ```
  - If date is omitted, default to `Sys.Date()`.
  - Slugify: `tolower(title)` → replace non-alphanumeric runs with `-` → strip
    leading/trailing `-`.
  - Compute `dir_name <- paste0("labnotes/", date, "_", slug)`.
  - Check the dir doesn't already exist; error if it does.
  - `dir.create(dir_name, recursive = TRUE)`.
  - Write `file.path(dir_name, "index.qmd")` with the front matter template above
    (title, description placeholder, author "Josh", date, one-element categories
    list, `draft: true`) and a trailing `{{< include ../_sessioninfo.qmd >}}` line.
  - Print a message: `Created <dir_name>/index.qmd`.

- [ ] Write `_scripts/README.md` documenting:
  - `Rscript _scripts/new_post.R "My Title"` — creates today's post
  - `Rscript _scripts/new_post.R "My Title" 2025-06-01` — creates a back-dated post
  - `Rscript _scripts/sync_papers.R` (task 07) — refreshes `papers.bib`

- [ ] Add `_scripts/` to `renv` awareness if it introduces new packages (the script
  itself only uses base R; no extra packages expected).

## Files changed

New: `_scripts/new_post.R`, `_scripts/README.md`

## Done when

- `Rscript _scripts/new_post.R "My Test Post"` creates
  `labnotes/<today>_my-test-post/index.qmd` with correct Quarto front matter.
- The created post appears in the blog listing after `quarto preview`.
- Running the command twice with the same title errors cleanly rather than
  overwriting.
