from scryfall_telegram.telegram.models import (
    InputMediaPhoto,
    SendMediaGroup,
    SendMessage,
    SendPhoto,
)

TEST_PHOTO = "https://c1.scryfall.com/file/scryfall-cards/png/front/a/d/ad98e518-4ec9-403e-a978-217244262c8f.png?1562439724"


class TestTelegramClient:
    def test_send_message(self, telegram, chat_id):
        resp = telegram.send_message(
            SendMessage(
                chat_id=chat_id, text="scryfall-telegram integration test message."
            )
        )
        resp.raise_for_status()

    def test_send_photo(self, telegram, chat_id):
        resp = telegram.send_photo(
            SendPhoto(
                chat_id=chat_id,
                photo=TEST_PHOTO,
                caption="scryfall-telegram integration test photo.",
            )
        )
        resp.raise_for_status()

    def test_send_media_group(self, telegram, chat_id):
        resp = telegram.send_media_group(
            SendMediaGroup(
                chat_id=chat_id,
                media=[
                    InputMediaPhoto(type="photo", media=TEST_PHOTO) for _ in range(3)
                ],
            )
        )
        resp.raise_for_status()
