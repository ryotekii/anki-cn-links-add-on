from pathlib import Path

from aqt import gui_hooks, mw
from aqt.reviewer import Reviewer
from aqt.webview import WebContent

from .search import search_character


BASE_PATH = Path(__file__).parent

mw.addonManager.setWebExports(
    __name__,
    r"web/.*\.(js|css)",
)


def add_web_resources(
    web_content: WebContent,
    context,
) -> None:
    if not isinstance(context, Reviewer):
        return

    addon_package = mw.addonManager.addonFromModule(__name__)

    web_content.css.append(
        f"/_addons/{addon_package}/web/hover.css"
    )

    web_content.js.append(
        f"/_addons/{addon_package}/web/hover.js"
    )


gui_hooks.webview_will_set_content.append(
    add_web_resources
)


def add_reviewer_bootstrap(html, card, context):
    if context not in ("reviewQuestion", "reviewAnswer"):
        return html

    config = mw.addonManager.getConfig("cn_links")
    hanzi_field = config["hanzi_field"]

    current_word = card.note()[hanzi_field]

    # Échapper ce qui pourrait poser problème dans JS.
    import json

    current_word_js = json.dumps(current_word)

    return html + f"""
    <script>
        window.cnLinksCurrentWord = {current_word_js};

        onUpdateHook.push(function () {{
            window.cnLinksInit();
        }});
    </script>
    """

gui_hooks.card_will_show.append(
    add_reviewer_bootstrap
)


def on_js_message(handled, message, context):
    if not isinstance(context, Reviewer):
        return handled

    if not message.startswith("cn-links:"):
        return handled

    data = message.removeprefix("cn-links:")

    character, current_word = data.split("|", 1)

    results = search_character(
        character,
        current_word,
    )

    return True, results

gui_hooks.webview_did_receive_js_message.append(
    on_js_message
)