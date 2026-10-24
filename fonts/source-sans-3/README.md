# Source Sans 3

The site's text font, self-hosted for both the website and the CV PDF.

- `*.otf`: Regular, It, Bold and BoldIt from Adobe's release 3.052R (<https://github.com/adobe-fonts/source-sans/releases/tag/3.052R>), unmodified, downloaded 2026-10-24. Used by the CV PDF (`_typst/typst-template.typ`, via `font-paths` in `cv.qmd`).
- `web/*.woff2`: Latin and Latin Extended subsets of weights 300, 400 and 600 (normal and italic) from the Fontsource npm package `@fontsource/source-sans-3` 5.3.0, unmodified. Used by the website through the `@font-face` rules in `css/fonts.scss`.
- License: SIL Open Font License 1.1 (`LICENSE.txt`), with Reserved Font Name "Source": redistribution is fine, but modified versions must be renamed.
