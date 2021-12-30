from textwrap import shorten
from typing import Sequence

from .query import Query
from .scryfall.models import Card
from .telegram.models import InlineKeyboardButton, InlineKeyboardMarkup


def initial_suggest_keyboard(query: Query) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Meant something else?",
                    callback_data=query.to_telegram_query(),
                )
            ]
        ]
    )


def alternatives_keyboard(
    cards: Sequence[Card], query: Query, prev: bool = False, next_: bool = False
) -> InlineKeyboardMarkup:
    res = InlineKeyboardMarkup(
        inline_keyboard=[[card_to_keyboard_button(c, query)] for c in cards]
    )
    current_page = query.page

    last_row = []
    if prev:
        query.page = current_page - 1
        last_row.append(
            InlineKeyboardButton(text="< Prev", callback_data=query.to_telegram_query())
        )
    if next_:
        query.page = current_page + 1
        last_row.append(
            InlineKeyboardButton(text="Next >", callback_data=query.to_telegram_query())
        )
    if last_row:
        res["inline_keyboard"].append(last_row)

    return res


def card_to_keyboard_button(card: Card, query: Query) -> InlineKeyboardButton:
    txt = (
        f"{shorten(card['name'], width=24, placeholder='...')} | {card['set'].upper()}"
    )

    mods = ""
    if card.get("full_art"):
        mods += "🖼️"

    if card.get("promo_types"):
        mods += " 🎨"

    if card["lang"] == "ja":
        mods += "🇯🇵"

    if mods:
        txt += " " + mods

    key_q = Query("", query.price_request, {}, {"c": card["id"]})
    return InlineKeyboardButton(text=txt, callback_data=key_q.to_telegram_query())
