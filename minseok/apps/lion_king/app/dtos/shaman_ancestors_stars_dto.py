from dataclasses import dataclass


@dataclass(frozen=True)
class AncestorsStarsQuery:
    id: int
    name: str


@dataclass(frozen=True)
class AncestorsStarsResponse:
    id: int
    name: str
