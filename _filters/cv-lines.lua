-- Lays out the lines of CV list items in HTML to match the PDF
-- (_typst/cv/typst-template.typ).
--
-- Splits each list item at its line breaks (`\` in cv.qmd) and wraps each line
-- in a span: `cv-line` for the first line and lines starting in bold (position
-- titles), `cv-detail` for the rest (institution, advisor, ...). css/cv.css
-- makes the spans blocks, with a hanging indent for `cv-line` and an indent for
-- `cv-detail`. The Typst template does the same itself, so this is HTML only.

if not quarto.doc.is_format("html") then
  return {}
end

local function first_inline(line)
  for _, el in ipairs(line) do
    if el.t ~= "Space" and el.t ~= "SoftBreak" then
      return el
    end
  end
end

local function split_lines(content)
  local result = pandoc.Inlines({})
  local line = pandoc.Inlines({})
  local function finish()
    local first = first_inline(line)
    local class = (#result == 0 or (first and first.t == "Strong")) and "cv-line" or "cv-detail"
    result:insert(pandoc.Span(line, { class = class }))
    line = pandoc.Inlines({})
  end
  for _, el in ipairs(content) do
    if el.t == "LineBreak" then
      finish()
    else
      line:insert(el)
    end
  end
  finish()
  return result
end

function BulletList(list)
  for _, item in ipairs(list.content) do
    for _, block in ipairs(item) do
      if block.t == "Para" or block.t == "Plain" then
        block.content = split_lines(block.content)
      end
    end
  end
  return list
end
