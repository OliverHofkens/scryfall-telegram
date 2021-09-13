from scryfall_telegram.scryfall.models import Prices
from scryfall_telegram.textmessage import _textify_prices


def test_textify_prices():
    prices = Prices(usd="1.2", usd_foil="5.0", eur="1.0", eur_foil="2.0", tix="0.3")
    res = _textify_prices(prices)
    assert isinstance(res, str)
