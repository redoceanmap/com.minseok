from dataclasses import dataclass


@dataclass(frozen=True)
class ZazuHornbillQuery:
    id: int
    name: str


@dataclass(frozen=True)
class ZazuHornbillResponse:
    id: int
    name: str
