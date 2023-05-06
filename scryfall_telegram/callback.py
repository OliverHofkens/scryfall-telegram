from typing import cast

import structlog

from .keyboard import alternatives_keyboard
from .query import Query
from .scryfall import service as scryfall
from .telegram import client as tg_client
from .telegram.models import (
    CallbackQuery,
    EditMessageMedia,
    EditMessageReplyMarkup,
    InputMediaPhoto,
    Message,
)
from .textmessage import _textify_prices

log = structlog.get_logger()


def handle_callback_query(query: CallbackQuery):
    try:
        msg = query["message"]
        data = query["data"]
    except KeyError:
        raise ValueError(f"Received unexpected callback query: {query}")

    tg_query = Query.from_telegram_query(cast(str, data), None)
    log.debug("reconstructed_query", query=str(tg_query))
    if "c" in tg_query.private_params:
        card_selected(cast(Message, msg), tg_query)
    else:
        # Or more suggestions are necessary:
        suggest_alternatives(cast(Message, msg), tg_query)


def suggest_alternatives(msg: Message, query: Query):
    telegram = tg_client.cached_telegram_client()

    # Suggest other results, including other printings:
    cards = scryfall.search_cards(query.to_scryfall_query(), unique="art")

    # Limit our results to 3 to not overpopulate the response keyboard:
    PAGE_SIZE = 3
    offset = (query.page - 1) * PAGE_SIZE
    card_page = cards[offset : offset + PAGE_SIZE]
    has_prev = query.page > 1
    has_next = len(cards) > offset + PAGE_SIZE

    keyboard = alternatives_keyboard(card_page, query, has_prev, has_next)
    update = EditMessageReplyMarkup(
        chat_id=msg["chat"]["id"], message_id=msg["message_id"], reply_markup=keyboard
    )
    telegram.edit_message_reply_markup(update)


def card_selected(msg: Message, query: Query):
    telegram = tg_client.cached_telegram_client()
    card = scryfall.single_card_by_id(query.private_params["c"])
    if not card:
        return
    card_img = scryfall.image_for_card(card, card["name"])

    photo = InputMediaPhoto(type="photo", media=card_img or "")
    if query.price_request:
        photo["caption"] = _textify_prices(card["prices"])

    update = EditMessageMedia(
        chat_id=msg["chat"]["id"], message_id=msg["message_id"], media=photo
    )
    telegram.edit_message_media(update)
