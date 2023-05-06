from scryfall_telegram.inline import scryfall_card_to_inline_query_article
from scryfall_telegram.scryfall.models import Card


def test_scryfall_card_to_inline_query_article():
    card = Card(
        id="abc123",
        name="Nyx-Fleece Ram",
        type_line="Enchantment Creature - Sheep",
        oracle_text="You win the game.",
        scryfall_uri="https://scryfall.com/card/a25/26/nyx-fleece-ram",
        image_uris={
            "normal": "https://c1.scryfall.com/file/scryfall-cards/png/front/a/d/ad98e518-4ec9-403e-a978-217244262c8f.png?1562439724"
        },
        prices={"eur": "666.99"},
    )

    assert scryfall_card_to_inline_query_article(card, "Nyx")
