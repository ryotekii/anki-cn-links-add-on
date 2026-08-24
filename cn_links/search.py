from aqt import mw


ADDON_NAME = "cn_links"


def get_config():
    return mw.addonManager.getConfig(ADDON_NAME)


def search_character(character: str) -> list[dict]:
    config = get_config()

    decks = config["decks"]
    hanzi_field = config["hanzi_field"]
    translation_field = config["translation_field"]

    if not decks:
        return []

    deck_queries = [
        f'deck:"{deck}"'
        for deck in decks
    ]

    deck_query = " OR ".join(deck_queries)

    search_query = (
        f"({deck_query}) "
        f"{hanzi_field}:*{character}*"
    )

    card_ids = mw.col.find_cards(search_query)

    results = []

    for card_id in card_ids:
        card = mw.col.get_card(card_id)
        note = card.note()

        word = note[hanzi_field]
        translation = note[translation_field]

        result = {
            "word": word,
            "translation": translation,
        }

        if result not in results:
            results.append(result)

    # Le caractère seul en premier
    results.sort(key=lambda result: result["word"] != character)

    return results