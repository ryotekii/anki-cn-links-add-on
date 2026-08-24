from pathlib import Path

from aqt import gui_hooks


BASE_PATH = Path(__file__).parent


def add_hover(html, card, context):
    if context not in ("reviewQuestion", "reviewAnswer"):
        return html

    js = (BASE_PATH / "hover.js").read_text(encoding="utf-8")
    css = (BASE_PATH / "hover.css").read_text(encoding="utf-8")

    return html + f"""
    <style>
    {css}
    </style>

    <script>
    {js}
    </script>
    """


gui_hooks.card_will_show.append(add_hover)