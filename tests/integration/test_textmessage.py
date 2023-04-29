from typing import List

from scryfall_telegram.telegram.models import Chat, Message, MessageEntity, User
from scryfall_telegram.textmessage import handle_message


def fake_message(
    chat_id: int, thread: int, text: str, entities: List[MessageEntity]
) -> Message:
    return {
        "date": 123,
        "chat": Chat(id=chat_id, username="Test chat", type="private"),
        "message_id": 1,
        "message_thread_id": thread,
        "from": User(id=1, first_name="Oliver"),
        "text": text,
        "entities": entities,
    }


def test_handle_start_command(telegram, any_group_id):
    chat_id, thread = any_group_id
    msg = fake_message(
        chat_id,
        thread,
        "/start",
        [MessageEntity(type="bot_command", offset=0, length=6)],
    )
    handle_message(msg)


def test_simple_basic_card(telegram, any_group_id):
    chat_id, thread = any_group_id
    msg = fake_message(chat_id, thread, "Hello [[ Nyx-Fleece Ram ]]", [])
    handle_message(msg)


def test_simple_multiple_cards(telegram, any_group_id):
    chat_id, thread = any_group_id
    msg = fake_message(
        chat_id, thread, "Hello [[delver secrets]] [[insectile aberration]]", []
    )
    handle_message(msg)


def test_simple_basic_card_prices(telegram, any_group_id):
    chat_id, thread = any_group_id
    msg = fake_message(chat_id, thread, "Hello [[ $ Nyx-Fleece Ram ]]", [])
    handle_message(msg)


def test_simple_multiple_cards_prices(telegram, any_group_id):
    chat_id, thread = any_group_id
    msg = fake_message(
        chat_id, thread, "Hello [[ $ delver secrets]] [[ € insectile aberration]]", []
    )
    handle_message(msg)
