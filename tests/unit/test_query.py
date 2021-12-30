import pytest

from scryfall_telegram.query import Query


@pytest.mark.parametrize(
    "tg_query, exp_free_text, exp_price, exp_set, exp_page",
    [
        ("nyx fleece", "nyx fleece", False, None, 1),
        ("$nyx fleece", "nyx fleece", True, None, 1),
        ("nyx fleece s:jou", "nyx fleece", False, "jou", 1),
        ("nyx fleece p=2", "nyx fleece", False, None, 2),
        ("$nyx-fleece s:jou p=2", "nyx-fleece", True, "jou", 2),
        ("c=123abc", "", False, None, 1),
    ],
)
def test_from_telegram_query(tg_query, exp_free_text, exp_price, exp_set, exp_page):
    q = Query.from_telegram_query(tg_query)

    assert q.free_text == exp_free_text
    assert q.price_request == exp_price
    assert q.set_code == exp_set
    assert q.page == exp_page

    assert q.to_telegram_query() == tg_query


@pytest.mark.parametrize(
    "tg_query, exp_sf_query",
    [
        ("nyx fleece", "nyx fleece"),
        ("$ nyx fleece", "nyx fleece"),
        ("nyx fleece s:jou", "nyx fleece s:jou"),
        ("nyx fleece s:jou p=1", "nyx fleece s:jou"),
    ],
)
def test_to_scryfall_query(tg_query, exp_sf_query):
    q = Query.from_telegram_query(tg_query)
    assert q.to_scryfall_query() == exp_sf_query
