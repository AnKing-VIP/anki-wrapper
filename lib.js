// Invoke cmd with a special context about the selection and patterns
function callCmd(cmd, beginPattern, endPattern) {
  // Param fetching
  const sel = window.getSelection();
  const node = sel.focusNode;
  if(sel.rangeCount <= 0 || !node)
    return;
  const range = sel.getRangeAt(0);

  // Context creation
  const toSend = {
    sel,
    node,
    range,
    beginIndex: null,
    endIndex: null,
    beginPatternMatch: null,
    endPatternMatch: null,
  };

  // Adding matches of patterns if they exist
  const text = node.textContent.substring(0, range.startOffset) + '\x1f' + node.textContent.substring(range.startOffset);
  const regex = new RegExp("(?<=^.*)(" + beginPattern + ").*?\x1f.*?(" + endPattern + ")")
  const match = regex.exec(text)

  if(match !== null && match.index !== null && match[0] !== null)
  {
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
  const sel = window.getSelection();

  sel.collapse(sel.focusNode, pos);
  if(end !== null)
    sel.extend(sel.focusNode, end);
}
