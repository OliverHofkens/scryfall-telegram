from typing import Dict, List, Optional

import orjson
from pyxdameraulevenshtein import damerau_levenshtein_distance

from .client import cached_scryfall_client
from .models import Card, Face


def search_cards(query: str) -> List[Card]:
    resp = cached_scryfall_client().search_cards(query, "name")

    if resp.status_code == 404:
        return []
    resp.raise_for_status()

    body = orjson.loads(resp.content)
    return body["data"]


def single_card_image(fuzzy_name: str, set_code: Optional[str] = None) -> Optional[str]:
    resp = cached_scryfall_client().named_card(fuzzy_name, set_code)

    if resp.status_code == 404:
        return None

    resp.raise_for_status()

    body = orjson.loads(resp.content)
    return _image_for_card(body, fuzzy_name)


def single_card_image_with_search_fallback(
    query: str, set_code: Optional[str] = None
) -> Optional[str]:
    hit = single_card_image(query, set_code)
    if hit:
        return hit

    # Format a search query:
    full_query = f"{query} s:{set_code}" if set_code else query

    hits = search_cards(full_query)
    if hits:
        return _image_for_card(hits[0], query)
    return None


def _image_for_card(
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
