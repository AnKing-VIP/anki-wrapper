/* Wrap selected text with pattern */
/* function wrap(begin, end) {
 *   built-in
 * }
 */


// Adapted from https://github.com/ankitects/anki/pull/3038 to work around issue when wrapping lists
// TODO: simplify logic
function wrap2(begin, end) {
  const {node: base} = this;
  const selection = getFieldInputSelection();
  const range = selection.getRangeAt(0);
  if (!range) {
      return;
  }

  let startParent = range.startContainer.parentNode;
  if (
      startParent !== base
      && startParent.tagName !== "ANKI-EDITABLE"
      && startParent?.firstChild === range.startContainer && range.startOffset === 0
  ) {
      range.setStartBefore(startParent);
  }

  let endParent = range.endContainer.parentNode;
  if (
      endParent !== base
      && endParent.tagName !== "ANKI-EDITABLE"
      && endParent?.lastChild === range.endContainer && (
          (range.endContainer.nodeType !== Node.ELEMENT_NODE
              && range.endOffset === range.endContainer.textContent?.length)
          || (range.endContainer.nodeType === Node.ELEMENT_NODE
              && range.endOffset === range.endContainer.childNodes.length)
      )
  ) {
      range.setEndAfter(endParent);
  }
  let expand;
  do {
      expand = false;
      if (
          startParent
          && startParent.parentNode !== base && startParent.parentNode.tagName !== "ANKI-EDITABLE" && startParent.parentNode?.firstChild === startParent
          && range.isPointInRange(startParent.parentNode, startParent.parentNode?.childNodes.length)
      ) {
          startParent = startParent.parentNode;
          range.setStartBefore(startParent);
          expand = true;
      }
      if (
          endParent && endParent.parentNode !== base && endParent.parentNode.tagName !== "ANKI-EDITABLE" && endParent.parentNode?.lastChild === endParent
          && range.isPointInRange(endParent.parentNode, 0)
      ) {
          endParent = endParent.parentNode;
          range.setEndAfter(endParent);
          expand = true;
      }
      if (range.endOffset === 0 && range.endContainer.tagName !== "ANKI-EDITABLE") {
          range.setEndBefore(range.endContainer);
          expand = true;
      }
  } while (expand);

  const fragment = range.extractContents();
  if (fragment.childNodes.length === 0) {
      document.execCommand("inserthtml", false, begin + end);
  } else {
      const div = document.createElement("div");
      for(const node of Array.from(fragment.childNodes)) {
        div.appendChild(node);
      }
      div.innerHTML = begin + div.innerHTML + end;
      for(const node of div.childNodes) {
        range.insertNode(node);
      }
  }
}

/* Move to end of pattern */
function moveEnd() {
  const {endIndex} = this;

  if(endIndex===null)
    return;

  moveCursor(endIndex);
}

/* Move to end of pattern, but inside */
function moveEndInside() {
  const {endIndex, endPatternMatch} = this;

  if(endIndex===null)
    return;

  moveCursor(endIndex - endPatternMatch.length);
}

/* Move to beginning of pattern */
function moveBegin() {
  const {beginIndex} = this;

  if(beginIndex===null)
    return;

  moveCursor(beginIndex);
}

/* Move to beginning of pattern, but inside */
function moveBeginInside() {
  const {beginIndex, beginPatternMatch} = this;

  if(beginIndex===null)
    return;

  moveCursor(beginIndex + beginPatternMatch.length);
}

/* Destroys selected pattern */
function unwrap() {
  const {beginIndex, beginPatternMatch, endIndex, endPatternMatch} = this;

  moveCursor(endIndex - endPatternMatch.length, endIndex);
  setFormat("delete");

  moveCursor(beginIndex, beginIndex + beginPatternMatch.length);
  setFormat("delete");
}


