from typing import List

from scryfall_telegram.telegram.models import Chat, Message, MessageEntity, User
from scryfall_telegram.textmessage import handle_message


def fake_message(chat_id: int, text: str, entities: List[MessageEntity]) -> Message:
    return {
        "date": 123,
        "chat": Chat(id=chat_id, username="Test chat", type="private"),
        "message_id": 1,
        "from": User(id=1, first_name="Oliver"),
        "text": text,
        "entities": entities,
    }


def test_handle_start_command(telegram, chat_id):
    msg = fake_message(
        chat_id, "/start", [MessageEntity(type="bot_command", offset=0, length=6)]
    )
    handle_message(msg)


def test_simple_basic_card(telegram, chat_id):
    msg = fake_message(chat_id, "Hello [[ Nyx-Fleece Ram ]]", [])
    handle_message(msg)


def test_simple_multiple_cards(telegram, chat_id):
    msg = fake_message(chat_id, "Hello [[delver secrets]] [[insectile aberration]]", [])
    handle_message(msg)


def test_simple_basic_card_prices(telegram, chat_id):
    msg = fake_message(chat_id, "Hello [[ $ Nyx-Fleece Ram ]]", [])
    handle_message(msg)


def test_simple_multiple_cards_prices(telegram, chat_id):
    msg = fake_message(
        chat_id, "Hello [[ $ delver secrets]] [[ € insectile aberration]]", []
    )
    handle_message(msg)
