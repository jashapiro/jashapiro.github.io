// Typst layout for the CV's PDF. cv.qmd uses this file as a template partial
// (replacing Quarto's default, which defines `article`); typst-show.typ, next
// to it, calls `cv` instead of `article`.
//
// Section headings sit in the left margin; list items and publications have
// no bullets and a hanging indent; pages after the first get a running header.

#let accent = rgb("#2f5597")
// Source Sans 3 (the site's font) is in the repo (fonts/source-sans-3, via
// `font-paths` in cv.qmd), so local and CI builds match; the rest are fallbacks
// (Typst has no generic "sans-serif", so DejaVu Sans, which Ubuntu always has,
// comes last)
#let fonts = ("Source Sans 3", "Helvetica", "Arial", "DejaVu Sans")
#let label-width = 1.3in
#let label-gap = 0.2in

// a list item's content split at its line breaks, as arrays of elements
#let item-lines(body) = {
  let children = if body.has("children") { body.children } else { (body,) }
  children.split(linebreak())
}

#let cv(
  title: none,
  lang: "en",
  region: "US",
  fontsize: 10pt,
  doc,
) = {
  set document(title: title)
  set page(
    paper: "us-letter",
    margin: (left: 0.7in + label-width + label-gap, right: 0.8in, top: 0.9in, bottom: 0.8in),
    // page numbers are in the header instead
    numbering: none,
    header: context {
      if counter(page).get().first() > 1 {
        set text(size: 0.85em)
        align(right)[#text(fill: accent, title) \ page #counter(page).display()]
      }
    },
  )
  set text(font: fonts, lang: lang, region: region, size: fontsize)
  set par(justify: false, leading: 0.5em, spacing: 0.85em, hanging-indent: 1em)
  // list items as plain paragraphs, so they get the hanging indent too
  // (Typst doesn't make paragraphs of tight list items)
  // (no space above the first item, so it lines up with a margin heading)
  show list: it => for (i, item) in it.children.enumerate() {
    block(above: if i == 0 { 0pt } else { 0.85em }, below: 0.85em, width: 100%, {
      // each line (`\` in cv.qmd) is its own paragraph: the first line and
      // position titles (lines starting in bold) at the outer edge, the rest
      // (institution, advisor, ...) indented
      set par(spacing: 0.5em)
      for (j, line) in item-lines(item.body).enumerate() {
        let first = line.find(c => c != [ ])
        if j == 0 or (first != none and first.func() == strong) {
          line.join()
        } else {
          block(inset: (left: 1em), spacing: 0.5em, par(hanging-indent: 0pt, line.join()))
        }
        parbreak()
      }
    })
  }
  show link: set text(fill: accent)

  // section headings (`##` in cv.qmd, level 1 here): right-aligned in the
  // margin, level with the first line of the section
  show heading.where(level: 1): it => block(
    above: 1.6em,
    below: 0pt,
    sticky: true,
    place(
      left,
      dx: -(label-width + label-gap),
      box(width: label-width, align(right, text(
        fill: accent,
        size: 0.95em,
        weight: "regular",
        tracking: 0.03em,
        upper(it.body),
      ))),
    ),
  )

  if title != none {
    block(below: 2em, text(size: 2em, fill: accent, title))
  }
  doc
}
