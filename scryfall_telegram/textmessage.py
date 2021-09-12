import re
from itertools import islice
from typing import List

from .scryfall import service as scryfall
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


def handle_plaintext(text: str, msg: Message):
    results = []

    # Find up to 10 matches in the text:
    for match in islice(_PATTERN.finditer(text), 0, 10):
        q, set_code = match.group(1, 2)
        res = scryfall.single_card_image_with_search_fallback(q, set_code)
        if res:
            results.append(res)

    if not results:
        return

    telegram = tg_client.cached_telegram_client()

    if len(results) == 1:
        telegram.send_photo(SendPhoto(chat_id=msg["chat"]["id"], photo=results[0]))
    else:
        telegram.send_media_group(
            SendMediaGroup(
                chat_id=msg["chat"]["id"],
                media=[InputMediaPhoto(type="photo", media=p) for p in results],
            )
        )


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


_CMD_START_TXT = """
Welcome to ScryfallBot!

*Usage*
ScryfallBot works in both _inline_ mode and in active mode.
Inline mode means you just tag @ScryfallBot and start typing while the results show up above your keyboard.
Tapping a result will send it in your chat. All Scryfall syntax is supported, for a full overview, see [the Scryfall syntax docs](https://scryfall.com/docs/syntax)
Active mode means you can add ScryfallBot to a chat and look up cards by typing [[ your card here ]] in chat.
You can find specific printings or limit the search to a set by adding the set code like this: [[ my card lookup | SET ]].

NOTE: Currently, the bot needs to be an admin in your chat in order to see messages without being explicitly mentioned...

*Questions, Improvements, Changes*
ScryfallBot is open source and lives on [Github here](https://github.com/OliverHofkens/scryfall-telegram).
If you have a great idea, feature request, or bug report, feel free to [open an issue here](https://github.com/OliverHofkens/scryfall-telegram/issues)

*Legal stuff*
- The code for this bot is licensed under the [MIT License](https://github.com/OliverHofkens/scryfall-telegram/blob/master/LICENSE), so you're free to change it!
- I am in no way associated or affiliated with Scryfall, I just use [their fantastic, public API](https://scryfall.com/docs/api).

"""
