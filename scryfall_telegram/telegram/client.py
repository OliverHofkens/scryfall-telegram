import os
from functools import lru_cache
from typing import Any

import requests
import structlog

from .models import (
    AnswerInlineQuery,
    EditMessageMedia,
    EditMessageReplyMarkup,
    SendMediaGroup,
    SendMessage,
    SendPhoto,
)

log = structlog.get_logger()
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

    def _post(self, url: str, body: Any):
        resp = self.session.post(_BASE_URL + _bot_token() + url, json=body)
        log.debug("telegram_response", url=url, body=body, status=resp.status_code)

        try:
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            log.error("http_error", body=e.response.text if e.response else None)

        return resp

    def answer_inline_query(self, answer: AnswerInlineQuery):
        return self._post("/answerInlineQuery", answer)

    def send_message(self, message: SendMessage):
        return self._post("/sendMessage", message)

    def send_photo(self, message: SendPhoto):
        return self._post("/sendPhoto", message)

    def send_media_group(self, message: SendMediaGroup):
        return self._post("/sendMediaGroup", message)

    def edit_message_reply_markup(self, reply_markup: EditMessageReplyMarkup):
        return self._post("/editMessageReplyMarkup", reply_markup)

    def edit_message_media(self, edit: EditMessageMedia):
        return self._post("/editMessageMedia", edit)
