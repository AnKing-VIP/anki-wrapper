// Invoke cmd with a special context about the selection and patterns
function callCmd(cmd, beginPattern, endPattern) {
  // Param fetching
  const sel = getFieldInputSelection()
  if (!sel) {
    return
  }
  const node = sel.focusNode

  if (sel.rangeCount <= 0 || !node)
    return
  const range = sel.getRangeAt(0)

  // Context creation
  const toSend = {
    sel,
    node: node,
    range,
    beginIndex: null,
    endIndex: null,
    beginPatternMatch: null,
    endPatternMatch: null,
  };

  // Adding matches of patterns if they exist
  const text = node.textContent.substring(0, range.startOffset) + '\x1f' + node.textContent.substring(range.startOffset)
  const regex = new RegExp("(?<=^.*)(" + beginPattern + ")(?:.(?!" + endPattern + "))*\x1f.*?(" + endPattern + ")", "g")
  const match = regex.exec(text)

  if (match !== null && match.index !== null && match[0] !== null) {
    toSend.beginIndex = match.index
    toSend.endIndex = match.index + match[0].length - 1
    toSend.beginPatternMatch = match[1]
    toSend.endPatternMatch = match[2]
  }
  cmd.call(toSend, beginPattern, endPattern)
}

// Move the cursor to pos. If end is provided, select the whole text
// If addRange is provided, add it as a new cursor
function moveCursor(pos, end = null) {
  const sel = getFieldInputSelection()

  sel.collapse(sel.focusNode, pos);
  if (end !== null)
    sel.extend(sel.focusNode, end);
}

function getFieldInputSelection() {
  // later anki versions have the field inputs inside a shadowroot and just calling window.getSelection() doesn't work
  const fieldSelection = window.getSelection()

  if (fieldSelection.focusNode.nodeName == "#text") {
    return fieldSelection;
  }

  let shadowRoot;
  if (fieldSelection.focusNode.querySelector(".field")) {
    shadowRoot = fieldSelection.focusNode.querySelector(".field").shadowRoot
  } else if (fieldSelection.focusNode.querySelector(".rich-text-editable")) {
    shadowRoot = fieldSelection.focusNode.querySelector(".rich-text-editable").shadowRoot
  } else {
    return null
  }
  return shadowRoot.getSelection()
}