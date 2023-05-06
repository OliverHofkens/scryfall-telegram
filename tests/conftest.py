import os

import pytest

from scryfall_telegram.logging import setup_logging
from scryfall_telegram.telegram.client import cached_telegram_client


def _env_or_skip(var_name: str):
    try:
        var = os.environ[var_name]
    except KeyError:
        pytest.skip(f"{var_name} missing from env.")
    return var


@pytest.fixture(scope="session", autouse=True)
def _setup_logging():
    setup_logging()


@pytest.fixture()
def bot_token(monkeypatch):
    stag_token = _env_or_skip("TELEGRAM_BOT_TOKEN_STAG")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", stag_token)


@pytest.fixture(scope="session")
def chat_id():
    id = _env_or_skip("TEST_CHAT_ID")
    return int(id)


@pytest.fixture(scope="session")
def supergroup_id():
    id = _env_or_skip("TEST_CHAT_SUPERGROUP_ID")
    return int(id)


@pytest.fixture(scope="session")
def supergroup_topic():
    id = _env_or_skip("TEST_CHAT_SUPERGROUP_TOPIC")
    return int(id)


@pytest.fixture(scope="session")
def channel_id():
    id = _env_or_skip("TEST_CHAT_CHANNEL_ID")
    return int(id)


@pytest.fixture(params=["chat_id", "supergroup_id", "channel_id"])
def any_group_id(request, chat_id, supergroup_id, supergroup_topic, channel_id):
    val = locals()[request.param]
    if request.param == "supergroup_id":
        return val, supergroup_topic
    else:
        return val, None


@pytest.fixture()
def telegram(bot_token):
    return cached_telegram_client()
