import os
from functools import lru_cache

import requests

from .models import (
    AnswerInlineQuery,
    EditMessageMedia,
    EditMessageReplyMarkup,
    SendMediaGroup,
    SendMessage,
    SendPhoto,
)

_BASE_URL = "https://api.telegram.org/"


@lru_cache()
def _bot_token() -> str:
    return "bot" + os.environ["TELEGRAM_BOT_TOKEN"]


@lru_cache()
def cached_telegram_client():
    return TelegramClient()


class TelegramClient:
    def __init__(self):
        self.session = requests.Session()

    def answer_inline_query(self, answer: AnswerInlineQuery):
        return self.session.post(
            _BASE_URL + _bot_token() + "/answerInlineQuery", json=answer
        )

    def send_message(self, message: SendMessage):
        return self.session.post(
            _BASE_URL + _bot_token() + "/sendMessage", json=message
        )

    def send_photo(self, message: SendPhoto):
        return self.session.post(_BASE_URL + _bot_token() + "/sendPhoto", json=message)

    def send_media_group(self, message: SendMediaGroup):
        return self.session.post(
            _BASE_URL + _bot_token() + "/sendMediaGroup", json=message
        )

    def edit_message_reply_markup(self, reply_markup: EditMessageReplyMarkup):
        return self.session.post(
            _BASE_URL + _bot_token() + "/editMessageReplyMarkup", json=reply_markup
        )

    def edit_message_media(self, edit: EditMessageMedia):
        return self.session.post(
            _BASE_URL + _bot_token() + "/editMessageMedia", json=edit
        )
