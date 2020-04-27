from .config import getUserOption
from aqt import gui_hooks, mw
import re

def add_css(cmd, editor):
    def _compose_css(name, css):
        if isinstance(css, list):
            css = '\n'.join(css)
        return (f".{name} {{\n"
                f"{css}\n"
                f"}}\n")

    cssToAdd = '\n'.join(_compose_css(name, css) for name, css in getUserOption(["buttons", cmd, "css"], default=None).items())

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

        # Wrap
        c = getUserOption(["buttons", cmd])
        [begin, end] = [c[i].replace("\\", "\\\\") for i in ['beginWrap', 'endWrap']]
        editor.web.eval(fr"wrap('{begin}', '{end}');")

    return result

def init(rightoptbuttons, editor):
    def _parse_style(config):
        config['icon'] = f"../../_addons/wrapper/user_files/icons/{config['icon']}"
        return config

    rightoptbuttons.extend([editor.addButton(
        cmd=cmd,
        func=param_wraps(cmd),
        **_parse_style(config['style']),
    ) for cmd, config in getUserOption("buttons").items()])

mw.addonManager.setWebExports(__name__, r"user_files/icons/.*")
gui_hooks.editor_did_init_buttons.append(init)
