from typing import cast

import orjson

from .callback import handle_callback_query
from .inline import handle_inline_query
from .telegram.models import TelegramUpdate
from .textmessage import handle_message


def handle_telegram_webhook(event, context):
    update = cast(TelegramUpdate, orjson.loads(event["body"]))

    callback_query = update.get("callback_query")
    if callback_query:
        handle_callback_query(callback_query)

    inline_query = update.get("inline_query")
    if inline_query:
        handle_inline_query(inline_query)

    msg = update.get("message")
    if msg:
        handle_message(msg)

    return orjson.dumps({"statusCode": 200})
