import os
from typing import cast

import orjson

from .callback import handle_callback_query
from .inline import handle_inline_query
from .telegram.models import TelegramUpdate
from .textmessage import handle_message


def handle_telegram_webhook(event, context):
    if os.environ["STAGE"] == "staging":
        print(event)

    update = cast(TelegramUpdate, orjson.loads(event["body"]))

    if callback_query := update.get("callback_query"):
        handle_callback_query(callback_query)

    if inline_query := update.get("inline_query"):
        handle_inline_query(inline_query)

    if msg := update.get("message"):
        handle_message(msg)

    # TODO: We might want to start a thread in this case, and reply in it?
    if channel_msg := update.get("channel_post"):
        handle_message(channel_msg)

    return orjson.dumps({"statusCode": 200})
