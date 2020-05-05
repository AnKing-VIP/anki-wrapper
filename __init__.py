from .config import getUserOption
from aqt import gui_hooks, mw 
from aqt.qt import QShortcut, QKeySequence
from aqt.editor import Editor
from aqt.webview import WebContent
import re
import os

addon_package = mw.addonManager.addonFromModule(__name__)
addon_path = os.path.dirname(__file__)
user_files_path = os.path.join(addon_path, "user_files")


def add_css(cmd, editor):
    config = getUserOption(["buttons", cmd, "css"], default=None)
    if not config:
        return

    def _compose_css(name, css):
        if isinstance(css, dict):
            css = ';\n'.join([*[f"{key}: {value}" for key, value in
                css.items()], ""])[:-1]
        if isinstance(css, list):
            css = '\n'.join(css)
        css = '\n  '.join(["", *css.split('\n')])[1:]
        return (f".{name} {{\n"
                f"{css}\n"
                f"}}\n")

    cssToAdd = '\n'.join(_compose_css(name, css) for name, css in config.items())

    prefix = fr"BEGIN WRAPPER CODE {cmd}"
    prefix_comment = "Please do not edit this section directly, this code is generated automatically. Modify config.json instead"
    suffix = r"END WRAPPER CODE"

    wrapper_code_new = (f"/* {prefix}\n"
                       f"{prefix_comment} */\n"
                       f"{cssToAdd}\n"
                       f"/* {suffix} */")

    wrapper_code_query = (f"/\* {prefix}.*\*/\n"
                         f"(?P<style>.*?)\n"
                         f"/\* {suffix} \*/")

    model = editor.note.model()
    css = model['css']
    def _save_css():
        model["css"] = css
        mw.col.models.save(model, updateReqs=False)

    match = re.search(wrapper_code_query, css, flags=re.S|re.M)
    if match is None:
        css += "\n" + wrapper_code_new
        _save_css()
    elif match.group("style") != cssToAdd :
        css = re.sub(wrapper_code_query, wrapper_code_new, css, flags=re.S|re.M)
        _save_css()

def param_wraps(cmd):
    def result(editor):
        # Add css
        add_css(cmd, editor)

        # Do the requested action
        c = getUserOption(["buttons", cmd])
        [begin, end] = [c[i].replace("\\", "\\\\") for i in ['beginWrap', 'endWrap']]
        editor.web.eval(fr"callCmd({c['action']}, '{begin}', '{end}');")

    return result

def init(rightoptbuttons, editor):
    def _parse_style(config):
        result = dict(**config)

        if not config.get("icon"):
            result['icon'] = None
        else:
            result['icon'] = os.path.join(user_files_path, f"icons/{result['icon']}")

        return result

    def add(config):
        def _addButtonInvisible(keys, func, **kwargs):
            QShortcut(  # type: ignore
                QKeySequence(keys), editor.widget, activated=lambda s=editor: func(s),
            )

        if config.get("visible", True):
            return editor.addButton
        else:
            return _addButtonInvisible

    buttons = [add(config)(
        cmd=cmd,
        func=param_wraps(cmd),
        **_parse_style(config.get("style", {})),
    ) for cmd, config in getUserOption("buttons").items()]
    rightoptbuttons.extend([i for i in buttons if i])

def on_webview_will_set_content(web_content: WebContent, editor):
    if isinstance(editor, Editor):
        web_content.js.append(f"/_addons/{addon_package}/lib.js")
        web_content.js.append(f"/_addons/{addon_package}/commands.js")
        web_content.js.append(os.path.join(user_files_path, "js.js"))


mw.addonManager.setWebExports(__name__, r"user_files/icons/.*")
mw.addonManager.setWebExports(__name__, r".*(css|js)")
gui_hooks.editor_did_init_buttons.append(init)
gui_hooks.webview_will_set_content.append(on_webview_will_set_content)
