from functools import lru_cache
from typing import Dict, List, Optional

import orjson
from pyxdameraulevenshtein import damerau_levenshtein_distance

from .client import cached_scryfall_client
from .models import Card, Face


@lru_cache(25)
def search_cards(query: str, unique: Optional[str] = "cards") -> List[Card]:
    resp = cached_scryfall_client().search_cards(query, unique, "name")

    if resp.status_code == 404:
        return []
    resp.raise_for_status()

    body = orjson.loads(resp.content)
    return body["data"]


@lru_cache(25)
def single_card(fuzzy_name: str, set_code: Optional[str] = None) -> Optional[Card]:
    resp = cached_scryfall_client().named_card(fuzzy_name, set_code)

    if resp.status_code == 404:
        return None

    resp.raise_for_status()

    return orjson.loads(resp.content)


@lru_cache(25)
def single_card_by_id(card_id: str) -> Optional[Card]:
    resp = cached_scryfall_client().card_by_id(card_id)

    if resp.status_code == 404:
        return None

    resp.raise_for_status()

    return orjson.loads(resp.content)


def single_card_image(fuzzy_name: str, set_code: Optional[str] = None) -> Optional[str]:
    card = single_card(fuzzy_name, set_code)
    if card:
        return image_for_card(card, fuzzy_name)
    return None


def single_card_with_search_fallback(
    query: str, set_code: Optional[str] = None
) -> Optional[Card]:
    hit = single_card(query, set_code)
    if hit:
        return hit

    # Format a search query:
    full_query = f"{query} s:{set_code}" if set_code else query

    hits = search_cards(full_query)
    if hits:
        return hits[0]
    return None


def image_for_card(
    card: Card, name_of_interest: str, preferred_format: str = "normal"
) -> Optional[str]:
    img_source = card.get("image_uris")

    # If no root images, a double faced card might have images per face:
    if not img_source and "card_faces" in card:
        img_source = _images_for_face_with_name(
            card["card_faces"] or [], name_of_interest
        )

    if not img_source:
        return None

    try:
        return img_source[preferred_format]
    except KeyError:
        return next(iter(img_source.values()))


def _images_for_face_with_name(
    faces: List[Face], name: str
) -> Optional[Dict[str, str]]:
    ordered = sorted(faces, key=lambda f: damerau_levenshtein_distance(name, f["name"]))
    return ordered[0]["image_uris"]
