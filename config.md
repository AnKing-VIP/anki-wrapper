* buttons: Main object. Specify every wrapper buttons to create
  + Key: The name of the command (free)
  + Value: Object
    - style: object specifying the style of the button itself. Any parameter can be skipped
      * icon: Path to the png icon in the user_files/icons/ folder. (If your file is "user_files/icons/hello.png", put "hello")
      * tip: Alt-text to display to the user
      * keys: Keyboard shortcut to the button (eg. "Shift+c")
      * label: Name to display if there is no icon
      * All parameters can be found in the [addButton function](https://github.com/ankitects/anki/blob/master/qt/aqt/editor.py#L211)
    - css: css classes to add when calling this button
      * Key: Name of the css class
      * Value: Style of the class. Can be either one-line (string) or multi-line (array of strings)
    - beginWrap: Left-wrapping text
    - endWrap: Right-wrapping text
