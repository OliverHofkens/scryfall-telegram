from typing import Dict, List, Optional, TypedDict


class Prices(TypedDict):
    usd: Optional[str]
    usd_foil: Optional[str]
    eur: Optional[str]
    eur_foil: Optional[str]
    tix: Optional[str]


class Face(TypedDict):
    name: str
    image_uris: Optional[Dict[str, str]]


class Card(TypedDict):
    id: str
    name: str
    lang: str
    # Supposedly not nullable, but sometimes `null` in reality
    type_line: Optional[str]
    oracle_text: Optional[str]
    scryfall_uri: str
    image_uris: Optional[Dict[str, str]]
    card_faces: Optional[List[Face]]
    prices: Prices
    set: str
    full_art: bool
    frame_effects: Optional[List]
    promo_types: Optional[List]
