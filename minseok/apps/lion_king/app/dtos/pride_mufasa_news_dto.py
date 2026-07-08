from dataclasses import dataclass


@dataclass(frozen=True)
class MufasaNewsQuery:
    id: int
    name: str


@dataclass(frozen=True)
class MufasaNewsResponse:
    id: int
    name: str
