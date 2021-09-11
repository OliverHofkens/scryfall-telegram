import pytest

from scryfall_telegram.scryfall import service


def test_search_card_by_name():
    res = service.search_cards("Nyx-Fleece Ram")
    assert len(res) == 1


@pytest.mark.parametrize(
    "name, set_code",
    [("Nyx-Fleece Ram", None), ("Nyx-Fleece Ram", "JOU"), ("bolas dragon god", None)],
)
def test_get_card_by_name(name, set_code):
    res = service.single_card_image(name, set_code)
    assert res


def test_get_dfc_by_name():
    front = service.single_card_image("Delver of Secrets")
    back = service.single_card_image("Insectile Aberration")

    assert front
    assert back
    assert front != back


@pytest.mark.parametrize(
    "names", [["Commit", "Memory", "Commit // Memory"], ["Stomp", "Bonecrusher Giant"]]
)
def test_get_split_cards_by_name(names):
    results = []
    for name in names:
        results.append(service.single_card_image(name))

    for res in results:
        assert res
        assert res == results[0]


@pytest.mark.parametrize(
    "name, set_code",
    [
        ("nyx", None),
        ("gatstaf", None),
        ("gatstaf", "SOI"),
    ],
)
def test_get_card_with_fallback(name, set_code):
    res = service.single_card_image_with_search_fallback(name, set_code)
    assert res
