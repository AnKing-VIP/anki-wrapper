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

<center><div style="vertical-align:middle;"><a href="https://www.theanking.com"><img src="https://raw.githubusercontent.com/AnKingMed/My-images/master/AnKing/TheAnKing-New.png?raw=true"></a></div></center>

<center>&nbsp;<a href="https://www.facebook.com/ankingmed"><img src="https://raw.githubusercontent.com/AnKingMed/My-images/master/Social/FB.png?raw=true"></a>
<a href="https://www.instagram.com/ankingmed"><img src="https://raw.githubusercontent.com/AnKingMed/My-images/master/Social/Instagram.png?raw=true"></a>
<a href="https://www.youtube.com/theanking"><img src="https://raw.githubusercontent.com/AnKingMed/My-images/master/Social/YT.png?raw=true"></a>
<a href="https://www.tiktok.com/@ankingmed"><img src="https://raw.githubusercontent.com/AnKingMed/My-images/master/Social/TikTok.png?raw=true"></a>
<a href="https://www.twitter.com/ankingmed"><img src="https://raw.githubusercontent.com/AnKingMed/My-images/master/Social/Twitter.png?raw=true"></a></center>

<div><center><a href="https://www.theanking.com/vip"><img src="https://raw.githubusercontent.com/AnKingMed/My-images/master/AnKing/Patreon.jpg?raw=true"></a></center></div>



<div><center><a href="https://courses.theanking.com"><img src="https://raw.githubusercontent.com/AnKingMed/My-images/master/AnKing/MasteryCourse.png?raw=true"></a></center></div>
