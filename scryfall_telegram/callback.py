from textwrap import shorten
from typing import Tuple
from uuid import UUID

from .scryfall import service as scryfall
from .scryfall.models import Card
from .telegram import client as tg_client
from .telegram.models import (
    CallbackQuery,
    EditMessageMedia,
    EditMessageReplyMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)


def handle_callback_query(query: CallbackQuery):
    try:
        msg = query["message"]
        data = query["data"]
    except KeyError:
        raise ValueError(f"Received unexpected callback query: {query}")

    try:
        # Either a result was selected:
        UUID(data)
    except ValueError:
        # Or more suggestions are necessary:
        suggest_alternatives(msg, data)
    else:
        card_selected(msg, data)


def suggest_alternatives(msg: Message, data: str):
    telegram = tg_client.cached_telegram_client()

    query, page = pop_page(data)
    # Suggest other results, including other printings:
    cards = scryfall.search_cards(query, unique="art")
    # Limit our results to 3 to not overpopulate the response keyboard:
    PAGE_SIZE = 3
    offset = (page - 1) * PAGE_SIZE
    cards = cards[offset : offset + PAGE_SIZE]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[card_to_keyboard_button(c)] for c in cards]
        + [[InlineKeyboardButton(text="More...", callback_data=query + f" p={page+1}")]]
    )
    update = EditMessageReplyMarkup(
        chat_id=msg["chat"]["id"], message_id=msg["message_id"], reply_markup=keyboard
    )
    telegram.edit_message_reply_markup(update)


def card_selected(msg: Message, data: str):
    telegram = tg_client.cached_telegram_client()
    card_img = scryfall.single_card_image_by_id(data)
    update = EditMessageMedia(
        chat_id=msg["chat"]["id"],
        message_id=msg["message_id"],
        media=InputMediaPhoto(type="photo", media=card_img or ""),
    )
    telegram.edit_message_media(update)


def pop_page(query: str) -> Tuple[str, int]:
    """
    Extracts our own 'page' param from the query,
    and returns the query without it.
    """
    parts = query.split()
    try:
        page_q = next(p for p in parts if p.startswith("p="))
    except StopIteration:
        return query, 1

    parts.remove(page_q)
    page = int(page_q.split("=")[1])
    return " ".join(parts), page


def card_to_keyboard_button(card: Card) -> InlineKeyboardButton:
    txt = (
        f"{shorten(card['name'], width=24, placeholder='...')} | {card['set'].upper()}"
    )
    if card.get("frame_effects"):
        txt += " 🎨"
    return InlineKeyboardButton(text=txt, callback_data=card["id"])
