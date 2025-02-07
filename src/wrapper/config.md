* buttons: Main object. Specify every wrapper buttons to create
  + Key: The name of the command (free)
  + Value: Object
    - action: The action to execute. Must be a function either in commands.js or user\_files/js.js
    - visible: Is the button visible, or is it only a shortcut 
    - style: object specifying the style of the button itself. Any parameter can be skipped
      * icon: Path to the icon in the user_files/icons/ folder. (If your file is "user_files/icons/hello.png", put "hello.png")
      * tip: Alt-text to display to the user
      * keys: Keyboard shortcut to the button (eg. "Shift+c")
      * label: Name to display if there is no icon
      * All parameters can be found in the [addButton function](https://github.com/ankitects/anki/blob/master/qt/aqt/editor.py#L211)
    - css: css classes to add when calling this button
      * Key: Name of the css class
      * Value: Object representing the style of the class. Can also be a one-line string or a multiline string (array of string)
    - beginWrap: Left-wrapping text
    - endWrap: Right-wrapping text
    - html: HTML files to add to templates when calling this button. The names are relative to the user_files/html folder.
      * front: list of files to add to front template.
      * back: list of files to add to back template.
