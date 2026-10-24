-- Formats the CV publication list.
--
-- Runs citeproc itself (Quarto only runs it after all user filters), then edits
-- the generated entries:
--   * bolds the author named in `highlight-author`: a name or a list of the forms
--     it takes in different papers (e.g. [Shapiro JA, Shapiro J])
--   * adds "*" after the authors listed for a citation key in
--     `equal-contribution`, e.g.
--       equal-contribution:
--         Andersen2012-ss: [Andersen EC, Gerke JP, Shapiro JA]
-- Names are matched as citeproc renders them, so they work for HTML and Typst.

local function words(name)
  local result = {}
  for word in pandoc.utils.stringify(name):gmatch("%S+") do
    table.insert(result, word)
  end
  return result
end

-- If the name `name_words` starts at inlines[i], returns the index of its last
-- Str and any punctuation that follows the name in that Str.
local function match_name(inlines, i, name_words)
  local j = i
  for w, word in ipairs(name_words) do
    local el = inlines[j]
    if not el or el.t ~= "Str" then
      return nil
    end
    if w < #name_words then
      if el.text ~= word or not (inlines[j + 1] and inlines[j + 1].t == "Space") then
        return nil
      end
      j = j + 2
    else
      local head, tail = el.text:match("^(.-)([,.]?)$")
      if head ~= word then
        return nil
      end
      return j, tail
    end
  end
end

local function name_inlines(name_words, suffix)
  local result = pandoc.Inlines({})
  for w, word in ipairs(name_words) do
    if w > 1 then
      result:insert(pandoc.Space())
    end
    result:insert(pandoc.Str(word))
  end
  if suffix ~= "" then
    result:insert(pandoc.Str(suffix))
  end
  return result
end

local function contains(names, name_words)
  local joined = table.concat(name_words, " ")
  for _, name in ipairs(names) do
    if table.concat(name, " ") == joined then
      return true
    end
  end
  return false
end

local function format_entry(inlines, self_names, equal_names)
  local result = pandoc.Inlines({})
  local i = 1
  while i <= #inlines do
    local done = false
    local candidates = {}
    for _, name in ipairs(self_names) do
      table.insert(candidates, name)
    end
    for _, name in ipairs(equal_names) do
      table.insert(candidates, name)
    end
    for _, name_words in ipairs(candidates) do
      local last, tail = match_name(inlines, i, name_words)
      if last then
        local is_self = contains(self_names, name_words)
        local is_equal = contains(equal_names, name_words)
        local name = name_inlines(name_words, is_equal and "*" or "")
        result:insert(is_self and pandoc.Strong(name) or pandoc.Span(name))
        if tail ~= "" then
          result:insert(pandoc.Str(tail))
        end
        i = last + 1
        done = true
        break
      end
    end
    if not done then
      result:insert(inlines[i])
      i = i + 1
    end
  end
  return result
end

function Pandoc(doc)
  local self_names = {}
  local highlight = doc.meta["highlight-author"] or {}
  if pandoc.utils.type(highlight) ~= "List" then
    highlight = { highlight }
  end
  for _, name in ipairs(highlight) do
    table.insert(self_names, words(name))
  end
  local equal = {}
  for key, names in pairs(doc.meta["equal-contribution"] or {}) do
    equal[key] = {}
    for _, name in ipairs(names) do
      table.insert(equal[key], words(name))
    end
  end

  doc = pandoc.utils.citeproc(doc)
  -- nothing left for Quarto's own citeproc pass to add
  doc.meta.bibliography = nil
  doc.meta.nocite = nil

  return doc:walk({
    Div = function(div)
      if not div.classes:includes("csl-entry") then
        return nil
      end
      local key = div.identifier:gsub("^ref%-", "")
      local function format_block(block)
        block.content = format_entry(block.content, self_names, equal[key] or {})
        return block
      end
      return div:walk({ Para = format_block, Plain = format_block })
    end,
  })
end
