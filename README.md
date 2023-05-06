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


---
### If you like these, please consider donating to this project

<p align="center">
<a href="https://www.ankingmed.com" rel="nofollow"><img src="https://raw.githubusercontent.com/AnKingMed/My-images/master/AnKing/AnKingSmall.png?raw=true"></a><a href="https://www.ankingmed.com" rel="nofollow"><img src="https://raw.githubusercontent.com/AnKingMed/My-images/master/AnKing/TheAnKing.png?raw=true"></a>
  <br>
  <a href="https://www.facebook.com/ankingmed" rel="nofollow"><img src="https://raw.githubusercontent.com/AnKingMed/My-images/master/Social/FB.png?raw=true"></a>     <a href="https://www.instagram.com/ankingmed" rel="nofollow"><img src="https://raw.githubusercontent.com/AnKingMed/My-images/master/Social/Instagram.png?raw=true"></a>     <a href="https://www.youtube.com/theanking" rel="nofollow"><img src="https://raw.githubusercontent.com/AnKingMed/My-images/master/Social/YT.png?raw=true"></a>     <a href="https://www.tiktok.com/@ankingmed" rel="nofollow"><img src="https://raw.githubusercontent.com/AnKingMed/My-images/master/Social/TikTok.png?raw=true"></a>     <a href="https://www.twitter.com/ankingmed" rel="nofollow"><img src="https://raw.githubusercontent.com/AnKingMed/My-images/master/Social/Twitter.png?raw=true"></a>
  <br>
<a href="https://www.ankipalace.com/membership" rel="nofollow"><img src="https://raw.githubusercontent.com/AnKingMed/My-images/master/AnKing/Patreon.jpg?raw=true"></a>
<br>
<b>Check out our <a href="https://courses.ankipalace.com/?utm_source=wrapper_add-on&amp;utm_medium=anki_add-on_page&amp;utm_campaign=mastery_course" rel="nofollow">Anki Mastery Course</a>! (The source of funding for this project)</b><br>
</p>

