from functools import lru_cache
from typing import Optional

import requests

_BASE_URL = "https://api.scryfall.com"


@lru_cache()
def cached_scryfall_client():
    return ScryfallClient()


class ScryfallClient:
    def __init__(self):
        self.session = requests.Session()

    def search_cards(
        self, query: str, order: Optional[str] = None, page: Optional[int] = 1
    ):
        return self.session.get(
            _BASE_URL + "/cards/search",
            params={
                "q": query,
                "order": order,
                "page": page,
                "include_multilingual": "true",
            },
        )

    def named_card(self, fuzzy_name: str, set_code: Optional[str] = None):
        return self.session.get(
            _BASE_URL + "/cards/named", params={"fuzzy": fuzzy_name, "set": set_code}
        )
