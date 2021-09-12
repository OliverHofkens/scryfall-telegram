from scryfall_telegram.scryfall.service import image_for_card

GOOD_URL = "https://scryfall.com"
BAD_URL = "https://sc.am"


def test_image_for_card_root():
    card = dict(id="123", name="test", image_uris=dict(small=BAD_URL, normal=GOOD_URL))

    assert image_for_card(card, "test", "normal") == GOOD_URL


def test_image_for_card_root_format_fallback():
    card = dict(id="123", name="test", image_uris=dict(small=GOOD_URL))

    assert image_for_card(card, "test", "normal") == GOOD_URL


def test_image_for_card_face():
    card = dict(
        id="123",
        name="test",
        card_faces=[
            dict(name="correct", image_uris=dict(normal=GOOD_URL)),
            dict(name="wrong", image_uris=dict(normal=BAD_URL)),
        ],
    )
    assert image_for_card(card, "correct", "normal") == GOOD_URL
    assert image_for_card(card, "wrong", "normal") == BAD_URL
    # Small typo's should be forgiven:
    assert image_for_card(card, "corretc", "normal") == GOOD_URL
