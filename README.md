Wrapper addon
===
Automatically create buttons and shortcut that manages wrapping and unwrapping text

Default buttons:
- Left justify (justify on the left, but center paragraph. Does not work on part of sentences)
- Move to end of cloze (ctrl+shift+space)
- Move to inner end of cloze (ctrl+space)
- Move to begining of cloze (ctrl+alt+shift+space)
- Move to inner begining of cloze (ctrl+shift+space)
- Unwrap current cloze (alt+shift+u)

Configuration
===
This addon allows you to create a list of buttons to add, with their own labels, shortcuts and icons.

For more details see [config.md](config.md)

Actions
===
The action field of [config.json](config.json) must be a javascript function.  
This can be either in commands.js or in the user files: user\_files/js.js.
If you want to create your own, look into commands.js and create a function in user\_files/js.js  
Then, you can acccept the begin and end pattern as parameters and additional parameter in the this parameter.  

The this parameter contains:
- sel: Current selection in the field
- node: Current field
- range: Current selection range
- beginIndex: Appearance of the openning pattern that contains the cursor
- endIndex: Appearance of the ending pattern that contains the cursor
- beginPatternMatch: Openning pattern captured
- endPatternMatch: Ending pattern captured
