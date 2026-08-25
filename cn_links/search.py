from aqt import mw

from anki.consts import (
    QUEUE_TYPE_NEW,
    QUEUE_TYPE_LRN,
    QUEUE_TYPE_REV,
    QUEUE_TYPE_DAY_LEARN_RELEARN,
)


def get_config():
    return mw.addonManager.getConfig("cn_links")


def get_knowledge(card) -> str:
    if card.queue == QUEUE_TYPE_NEW:
        return "new"

    if card.queue in (
        QUEUE_TYPE_LRN,
        QUEUE_TYPE_DAY_LEARN_RELEARN,
    ):
        return "learning"

    if card.queue == QUEUE_TYPE_REV:
        if card.ivl >= 21:
            return "mature"
        return "learning"

    return "new"


def search_character(
    character: str,
    current_word: str | None = None,
) -> list[dict]:
    config = get_config()

    decks = config["decks"]
    hanzi_field = config["hanzi_field"]
    translation_field = config["translation_field"]
    max_results = config.get("max_results", 10)

    results_by_word = {}

    for deck_name, priority in sorted(
        decks.items(),
        key=lambda item: item[1],
    ):
        search_query = (
            f'deck:"{deck_name}" '
            f'{hanzi_field}:*{character}*'
        )

        card_ids = mw.col.find_cards(search_query)

        for card_id in card_ids:
            card = mw.col.get_card(card_id)
            note = card.note()
            word = note[hanzi_field]

            if current_word and word == current_word:
                continue

            if word in results_by_word:
                continue

            results_by_word[word] = {
                "word": word,
                "translation": note[translation_field],
                "knowledge": get_knowledge(card),
                "priority": priority,
            }

    results = list(results_by_word.values())

    results.sort(
        key=lambda result: (
            result["word"] != character,
            result["priority"],
            result["word"],
        )
    )
    
    results = results[:max_results]

    for result in results:
        del result["priority"]

    return results