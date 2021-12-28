import pytest

from scryfall_telegram import callback


@pytest.mark.parametrize(
    "query, exp",
    [
        ("nyx-fleece", 1),
        ("nyx-fleece s:jou", 1),
        ("nyx-fleece p=2", 2),
        ("nyx-fleece p=10 s:jou", 10),
    ],
)
def test_pop_page(query, exp):
    new_q, res = callback.pop_page(query)
    assert res == exp
    assert "p=" not in new_q
