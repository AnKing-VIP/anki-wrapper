import json
import os
import re
from typing import Callable, Dict, List

from aqt import gui_hooks, mw
from aqt.editor import Editor
from aqt.qt import QKeySequence, QShortcut
from aqt.webview import WebContent

from .config import getUserOption

ADDON_PACKAGE_NAME = mw.addonManager.addonFromModule(__name__)
ADDON_PATH = os.path.dirname(__file__)
USER_FILES_PATH = os.path.join(ADDON_PATH, "user_files")


def add_css_to_model(cmd: str, model):
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

    prefix = rf"BEGIN WRAPPER CODE {cmd}"
    prefix_comment = "Please do not edit this section directly, this code is generated automatically. Modify config.json instead"
    suffix = r"END WRAPPER CODE"

    wrapper_code_new = (
        f"/* {prefix}\n" f"{prefix_comment} */\n" f"{cssToAdd}\n" f"/* {suffix} */"
    )

    wrapper_code_query = f"/\* {prefix}.*\*/\n" f"(?P<style>.*?)\n" f"/\* {suffix} \*/"

    css = model["css"]

    match = re.search(wrapper_code_query, css, flags=re.S | re.M)
    if match is None:
        css += "\n" + wrapper_code_new
    elif match.group("style") != cssToAdd:
        css = re.sub(wrapper_code_query, wrapper_code_new, css, flags=re.S | re.M)

    model["css"] = css

def add_html_to_model(cmd: str, model):
    config = getUserOption(["buttons", cmd, "html"], default=None)
    if not config:
        return

    def read_html(filename: str) -> str:
        with open(os.path.join(USER_FILES_PATH, "html", filename), "r", encoding="utf-8") as f:
            return f.read()

    sides_html = {
        "qfmt": "\n".join(read_html(filename) for filename in config.get("front", [])),
        "afmt": "\n".join(read_html(filename) for filename in config.get("back", []))
    }

    prefix = rf"BEGIN WRAPPER CODE {cmd}"
    prefix_comment = "Please do not edit this section directly, this code is generated automatically. Modify config.json instead"
    suffix = r"END WRAPPER CODE"

    for tmpl in model["tmpls"]:
        for side, html in sides_html.items():
            wrapper_code_new = (
                f"<!-- {prefix}\n" f"{prefix_comment} -->\n" f"{html}\n" f"<!-- {suffix} -->"
            )
            wrapper_code_query = f"<!-- {prefix}.*-->\n" f"(?P<html>.*?)\n" f"<!-- {suffix} -->"
            template_contents = tmpl[side]
            match = re.search(wrapper_code_query, template_contents, flags=re.S | re.M)
            if match is None:
                template_contents += "\n" + wrapper_code_new
            elif match.group("html") != html:
                template_contents = re.sub(wrapper_code_query, wrapper_code_new, template_contents, flags=re.S | re.M)
            tmpl[side] = template_contents


def init(rightoptbuttons: List[str], editor: Editor):
    def _param_wraps(cmd: str) -> Callable[[Editor], None]:
        def result(editor: Editor):
            model = editor.note.model()
            add_css_to_model(cmd, model)
            add_html_to_model(cmd, model)
            mw.col.models.save(model, updateReqs=False)

            # Do the requested action
            c = getUserOption(["buttons", cmd])
            begin = c["beginWrap"]
            end = c["endWrap"]
            editor.web.eval(rf"callCmd({c['action']}, {json.dumps(begin)}, {json.dumps(end)});")

        return result

    def _parse_style(config) -> Dict:
        result = dict(**config)

        if not config.get("icon"):
            result["icon"] = None
        else:
            result["icon"] = os.path.join(USER_FILES_PATH, f"icons/{result['icon']}")

        return result

    def _add_btn(config) -> Callable:
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
        _add_btn(config)(
            cmd=cmd,
            func=_param_wraps(cmd),
            **_parse_style(config.get("style", {})),
            id=f"meta-wrapper-btn-{cmd}",
        )
        for cmd, config in getUserOption("buttons").items()
    ]
    rightoptbuttons.extend([i for i in buttons if i])


gui_hooks.editor_did_init_buttons.append(init)

mw.addonManager.setWebExports(__name__, r"user_files/icons/.*")
mw.addonManager.setWebExports(__name__, r".*(css|js)")


def on_webview_will_set_content(web_content: WebContent, editor):
    # Workaround to a bug in v2.1.50.
    # https://forums.ankiweb.net/t/2-1-50-editor-wont-show-when-addons-load-many-js-files/19036
    def append_js_to_body(src: str):
        web_content.body += f'<script src="{src}"></script>'

    if isinstance(editor, Editor):
        append_js_to_body(f"/_addons/{ADDON_PACKAGE_NAME}/lib.js")
        append_js_to_body(f"/_addons/{ADDON_PACKAGE_NAME}/commands.js")
        append_js_to_body(f"/_addons/{ADDON_PACKAGE_NAME}/user_files/js.js")
        web_content.css.append(f"/_addons/{ADDON_PACKAGE_NAME}/btn.css")


gui_hooks.webview_will_set_content.append(on_webview_will_set_content)
