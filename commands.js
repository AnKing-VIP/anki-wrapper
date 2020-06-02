/* Wrap selected text with pattern */
/* function wrap(begin, end) {
 *   built-in
 * }
 */

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


