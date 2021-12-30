import re
from itertools import islice
from typing import List, Optional, Tuple

from .keyboard import initial_suggest_keyboard
from .query import Query
from .scryfall import service as scryfall
from .scryfall.models import Prices
from .telegram import client as tg_client
from .telegram.models import (
    InputMediaPhoto,
    Message,
    MessageEntity,
    SendMediaGroup,
    SendMessage,
    SendPhoto,
)

_PATTERN = re.compile(r"\[\[\s*([^|]+?)(?:\s*\|\s*(\w{3}))?\s*\]\]")


def handle_message(msg: Message):
    # Handle any [[ references ]] before checking for commands etc.
    contents = msg.get("text", "") or ""
    if contents:
        handle_plaintext(contents, msg)

    entities = msg.get("entities", [])
    if entities:
        handle_entities(contents, entities, msg)


def _textify_prices(prices: Prices) -> str:
    rows = []
    for field, price in prices.items():
        if not price:
            continue

        symbol = "🌟" if "foil" in field else ""

        if "usd" in field:
            market = "TCGplayer" + symbol
            currency = "$"
        elif "eur" in field:
            market = "Cardmarket" + symbol
            currency = "€"
        else:
            market = "MTGO"
            currency = "TIX"

        rows.append(f"{market}: {price}{currency}")

    return "\n".join(rows)


def _send_single_result(
    chat_id: int, image: Optional[str], prices: Optional[Prices], orig_query: Query
):
    telegram = tg_client.cached_telegram_client()

    keyboard = initial_suggest_keyboard(orig_query)
    if image:
        photo = SendPhoto(chat_id=chat_id, photo=image, reply_markup=keyboard)
        if prices:
            photo["caption"] = _textify_prices(prices)
        telegram.send_photo(photo)
    elif prices:
        telegram.send_message(
            SendMessage(
                chat_id=chat_id, text=_textify_prices(prices), reply_markup=keyboard
            )
        )


def _send_multiple_results(
    chat_id: int, results: List[Tuple[Optional[str], Optional[Prices]]]
):
    telegram = tg_client.cached_telegram_client()

    media = []
    for img, prices in results:
        photo = InputMediaPhoto(type="photo", media=img or "")
        if prices:
            photo["caption"] = _textify_prices(prices)
        media.append(photo)

    telegram.send_media_group(SendMediaGroup(chat_id=chat_id, media=media))


def handle_plaintext(text: str, msg: Message):
    results: List[Tuple[Optional[str], Optional[Prices]]] = []

    # Find up to 10 matches in the text:
    for match in islice(_PATTERN.finditer(text), 0, 10):
        q = Query.from_telegram_query(*match.group(1, 2))
        res = scryfall.single_card_with_search_fallback(q.free_text, q.set_code)

        if res:
            img = scryfall.image_for_card(res, q.free_text)
            prices = res["prices"] if q.price_request else None
            if img or prices:
                results.append((img, prices))

    if not results:
        return

    if len(results) == 1:
        _send_single_result(msg["chat"]["id"], *results[0], q)
    else:
        _send_multiple_results(msg["chat"]["id"], results)


def handle_entities(text: str, entities: List[MessageEntity], msg: Message):
    telegram = tg_client.cached_telegram_client()

    for entity in entities:
        if entity["type"] != "bot_command":
            continue

        offset = entity["offset"]
        length = entity["length"]
        cmd_text = text[offset : offset + length]

        if cmd_text == "/start":
            telegram.send_message(
                SendMessage(
                    chat_id=msg["chat"]["id"],
                    parse_mode="Markdown",
                    disable_web_page_preview=True,
                    text=_CMD_START_TXT,
                )
            )
        elif cmd_text == "/chatid":
            telegram.send_message(
                SendMessage(chat_id=msg["chat"]["id"], text=str(msg["chat"]["id"]))
            )


_CMD_START_TXT = """
Welcome to ScryfallBot!

*Usage*
ScryfallBot works in both _inline_ mode and in active mode.

Inline mode means you just tag @ScryfallBot and start typing while the results show up above your keyboard.
Tapping a result will send it in your chat. All Scryfall syntax is supported, for a full overview, see [the Scryfall syntax docs](https://scryfall.com/docs/syntax)

Active mode means you can add ScryfallBot to a chat and look up cards by typing [[ your card here ]] in chat.
The bot will search up to 10 cards per message.
You can find specific printings or limit the search to a set by adding the set code like this: [[ my card lookup | SET ]].
If you start the query with a '$' or '€' sign, the bot will include price information about the card: [[ $ nyx-fleece ]].

NOTE: Currently, the bot needs to be an admin in your chat in order to see messages without being explicitly mentioned...

*Questions, Improvements, Changes*
ScryfallBot is open source and lives on [Github here](https://github.com/OliverHofkens/scryfall-telegram).
If you have a great idea, feature request, or bug report, feel free to [open an issue here](https://github.com/OliverHofkens/scryfall-telegram/issues)

*Legal stuff*
- The code for this bot is licensed under the [MIT License](https://github.com/OliverHofkens/scryfall-telegram/blob/master/LICENSE), so you're free to change it!
- I am in no way associated or affiliated with Scryfall, I just use [their fantastic, public API](https://scryfall.com/docs/api).

"""
