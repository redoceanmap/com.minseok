from dataclasses import dataclass


@dataclass(frozen=True)
class NalaQueenQuery:
    id: int
    name: str


@dataclass(frozen=True)
class NalaQueenResponse:
    id: int
    name: str
