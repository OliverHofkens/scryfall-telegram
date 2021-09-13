import os

import pytest

from scryfall_telegram.telegram.client import cached_telegram_client


@pytest.fixture()
def bot_token(monkeypatch):
    try:
        stag_token = os.environ["TELEGRAM_BOT_TOKEN_STAG"]
    except KeyError:
        pytest.skip("TELEGRAM_BOT_TOKEN_STAG missing from env.")

    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", stag_token)


@pytest.fixture(scope="session")
def chat_id():
    try:
        id = os.environ["TEST_CHAT_ID"]
    except KeyError:
        pytest.skip("TEST_CHAT_ID missing from env.")

    return int(id)


@pytest.fixture()
def telegram(bot_token):
    return cached_telegram_client()
