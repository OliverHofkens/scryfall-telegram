from .scryfall import service as scryfall
from .scryfall.models import Card
from .telegram import client as tg
from .telegram.models import (
    AnswerInlineQuery,
    InlineQuery,
    InlineQueryResultArticle,
    InlineQueryResultPhoto,
    InputTextMessageContent,
)


def handle_inline_query(query: InlineQuery):
    query_str = query["query"]
    if not query_str:
        return

    results = scryfall.search_cards(query_str)

    response = AnswerInlineQuery(
        inline_query_id=query["id"],
        results=[scryfall_card_to_inline_query_photo(c) for c in results[:50]],
    )

    telegram = tg.cached_telegram_client()
    telegram.answer_inline_query(response)


def scryfall_card_to_inline_query_article(card: Card) -> InlineQueryResultArticle:
    img = card.get("image_uris", {}) or {}
    thumbnail = img.get("art_crop", img.get("small", None))

    return InlineQueryResultArticle(
        type="article",
        id=card["id"],
        title=card["name"],
        url=card["scryfall_uri"],
        description=card.get("oracle_text", card["type_line"]),
        thumb_url=thumbnail,
        hide_url=True,
        input_message_content=InputTextMessageContent(
            message_text=card["scryfall_uri"], disable_web_page_preview=False
        ),
    )


def scryfall_card_to_inline_query_photo(card: Card) -> InlineQueryResultPhoto:
    img = card.get("image_uris", {}) or {}
    # TODO: Find a better hosted fallback or host ourselves?
    fallback_img = (
        "https://gamepedia.cursecdn.com/mtgsalvation_gamepedia/f/f8/Magic_card_back.jpg"
    )

    return InlineQueryResultPhoto(
        type="photo",
        id=card["id"],
        title=card["name"],
        photo_url=img.get("large", fallback_img),
        thumb_url=img.get("small", fallback_img),
        # https://scryfall.com/docs/api/images
        photo_width=672,
        photo_height=936,
        caption=f"[Details on Scryfall.com]({card['scryfall_uri']})",
        parse_mode="Markdown",
    )
