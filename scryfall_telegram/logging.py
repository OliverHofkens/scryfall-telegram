import logging
import os

import structlog


def setup_logging(**context):
    min_level = logging.DEBUG if os.environ["STAGE"] == "staging" else logging.WARNING

    structlog.configure_once(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(min_level),
        cache_logger_on_first_use=True,
    )
    structlog.contextvars.clear_contextvars()
    if context:
        bind(**context)


def bind(**context):
    structlog.contextvars.bind_contextvars(**context)
