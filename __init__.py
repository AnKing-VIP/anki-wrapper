import os
import re
from typing import Callable, Dict, List

from aqt import gui_hooks, mw
from aqt.editor import Editor
from aqt.qt import QKeySequence, QShortcut
from aqt.webview import WebContent

from .config import getUserOption

addon_package = mw.addonManager.addonFromModule(__name__)
addon_path = os.path.dirname(__file__)
user_files_path = os.path.join(addon_path, "user_files")


def add_css_to_model(cmd: str, editor: Editor):
    config = getUserOption(["buttons", cmd, "css"], default=None)
    if not config:
        return

    def _compose_css(name: str, css: dict) -> str:
        if isinstance(css, dict):
            css = ";\n".join([*[f"{key}: {value}" for key, value in css.items()], ""])[
                :-1
            ]
        if isinstance(css, list):
            css = "\n".join(css)
        css = "\n  ".join(["", *css.split("\n")])[1:]
        return f".{name} {{\n" f"{css}\n" f"}}\n"

    cssToAdd = "\n".join(_compose_css(name, css) for name, css in config.items())

    prefix = fr"BEGIN WRAPPER CODE {cmd}"
    prefix_comment = "Please do not edit this section directly, this code is generated automatically. Modify config.json instead"
    suffix = r"END WRAPPER CODE"

    wrapper_code_new = (
        f"/* {prefix}\n" f"{prefix_comment} */\n" f"{cssToAdd}\n" f"/* {suffix} */"
    )

    wrapper_code_query = f"/\* {prefix}.*\*/\n" f"(?P<style>.*?)\n" f"/\* {suffix} \*/"

    model = editor.note.model()
    css = model["css"]

    def _save_css():
        model["css"] = css
        mw.col.models.save(model, updateReqs=False)

    match = re.search(wrapper_code_query, css, flags=re.S | re.M)
    if match is None:
        css += "\n" + wrapper_code_new
        _save_css()
    elif match.group("style") != cssToAdd:
        css = re.sub(wrapper_code_query, wrapper_code_new, css, flags=re.S | re.M)
        _save_css()


def param_wraps(cmd: str) -> Callable[[Editor], None]:
    def result(editor: Editor):
        # Add css
        add_css_to_model(cmd, editor)

        # Do the requested action
        c = getUserOption(["buttons", cmd])
        [begin, end] = [c[i].replace("\\", "\\\\") for i in ["beginWrap", "endWrap"]]
        editor.web.eval(fr"callCmd({c['action']}, '{begin}', '{end}');")

    return result


def init(rightoptbuttons: List[str], editor: Editor):
    def _parse_style(config) -> Dict:
        result = dict(**config)

        if not config.get("icon"):
            result["icon"] = None
        else:
            result["icon"] = os.path.join(user_files_path, f"icons/{result['icon']}")

        return result

    def add_btn(config) -> Callable:
        def _addButtonInvisible(keys, func, **kwargs):
            QShortcut(  # type: ignore
                QKeySequence(keys),
                editor.widget,
                activated=lambda s=editor: func(s),
            )

        if config.get("visible", True):
            return editor.addButton
        else:
            return _addButtonInvisible

    buttons = [
        add_btn(config)(
            cmd=cmd,
            func=param_wraps(cmd),
            **_parse_style(config.get("style", {})),
            id=f"meta-wrapper-btn-{cmd}"
        )
        for cmd, config in getUserOption("buttons").items()
    ]
    rightoptbuttons.extend([i for i in buttons if i])


def on_webview_will_set_content(web_content: WebContent, editor):
    if isinstance(editor, Editor):
        web_content.js.append(f"/_addons/{addon_package}/lib.js")
        web_content.js.append(f"/_addons/{addon_package}/commands.js")
        web_content.js.append(f"/_addons/{addon_package}/user_files/js.js")
        web_content.css.append(f"/_addons/{addon_package}/btn.css")


mw.addonManager.setWebExports(__name__, r"user_files/icons/.*")
mw.addonManager.setWebExports(__name__, r".*(css|js)")
gui_hooks.editor_did_init_buttons.append(init)
gui_hooks.webview_will_set_content.append(on_webview_will_set_content)
