from typing import cast

import orjson
import structlog

from .callback import handle_callback_query
from .inline import handle_inline_query
from .logging import setup_logging
from .telegram.models import TelegramUpdate
from .textmessage import handle_message

log = structlog.get_logger()


def handle_telegram_webhook(event, context):
    setup_logging(request_id=event["requestContext"]["requestId"])
    log.debug("got_update", data=event)

    update = cast(TelegramUpdate, orjson.loads(event["body"]))

    if callback_query := update.get("callback_query"):
        log.debug("callback_query", query=callback_query)
        handle_callback_query(callback_query)

    if inline_query := update.get("inline_query"):
        log.debug("inline_query", query=inline_query)
        handle_inline_query(inline_query)

    if msg := update.get("message"):
        log.debug("message", message=msg)
        handle_message(msg)

    # TODO: We might want to start a thread in this case, and reply in it?
    if channel_msg := update.get("channel_post"):
        log.debug("channel_post", message=channel_msg)
        handle_message(channel_msg)

    log.debug("success")
    return orjson.dumps({"statusCode": 200})
