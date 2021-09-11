from typing import cast

import orjson

from .inline import handle_inline_query
from .telegram.models import TelegramUpdate
from .textmessage import handle_message


def handle_telegram_webhook(event, context):
    update = cast(TelegramUpdate, orjson.loads(event["body"]))

    inline_query = update.get("inline_query")
    if inline_query:
        handle_inline_query(inline_query)

    msg = update.get("message")
    if msg:
        handle_message(msg)

    return orjson.dumps({"statusCode": 200})
