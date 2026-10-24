// Replaces Quarto's default typst-show.typ partial, which calls `article`
// with every option Quarto knows about; this passes only what `cv` (in
// typst-template.typ) uses.
#show: doc => cv(
$if(title)$
  title: [$title$],
$endif$
$if(lang)$
  lang: "$lang$",
$endif$
$if(region)$
  region: "$region$",
$endif$
$if(fontsize)$
  fontsize: $fontsize$,
$endif$
  doc,
)
