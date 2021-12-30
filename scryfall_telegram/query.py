from typing import Dict, Optional


class Query:
    def __init__(
        self,
        free_text: str,
        price_request: bool,
        scryfall_params: Dict[str, str],
        private_params: Dict[str, str],
    ):
        self.free_text = free_text
        self.price_request = price_request
        self.scryfall_params = scryfall_params
        self.private_params = private_params

    @classmethod
    def from_telegram_query(cls, q: str, set_code: Optional[str] = None) -> "Query":
        parts = q.split()

        scryfall_params_str = [p for p in parts if ":" in p]
        scryfall_params = {}
        for p in scryfall_params_str:
            key, val = p.split(":")
            scryfall_params[key] = val
            parts.remove(p)

        if set_code:
            scryfall_params["s"] = set_code

        private_params_str = [p for p in parts if "=" in p]
        private_params = {}
        for p in private_params_str:
            key, val = p.split("=")
            private_params[key] = val
            parts.remove(p)

        free_text = " ".join(parts)
        price_request = False
        if free_text.startswith("$") or free_text.startswith("€"):
            price_request = True
            free_text = free_text.lstrip("$€").lstrip()
        return cls(free_text, price_request, scryfall_params, private_params)

    @property
    def set_code(self) -> Optional[str]:
        return (
            self.scryfall_params.get("s")
            or self.scryfall_params.get("set")
            or self.scryfall_params.get("e")
            or self.scryfall_params.get("edition")
        )

    @property
    def page(self) -> int:
        return int(self.private_params.get("p", 1))

    @page.setter
    def page(self, page: int):
        self.private_params["p"] = str(page)

    def to_scryfall_query(self) -> str:
        q = self.free_text
        for k, v in self.scryfall_params.items():
            q += f" {k}:{v}"
        return q.strip()

    def to_telegram_query(self) -> str:
        q = self.free_text
        if self.price_request:
            q = "$" + q
        for k, v in self.scryfall_params.items():
            q += f" {k}:{v}"
        for k, v in self.private_params.items():  # type:ignore
            q += f" {k}={v}"
        return q.strip()
