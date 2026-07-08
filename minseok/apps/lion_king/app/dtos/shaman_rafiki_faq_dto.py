from dataclasses import dataclass


@dataclass(frozen=True)
class RafikiFaqQuery:
    id: int
    name: str


@dataclass(frozen=True)
class RafikiFaqResponse:
    id: int
    name: str
