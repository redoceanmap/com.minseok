from dataclasses import dataclass


@dataclass(frozen=True)
class SimbaKingQuery:
    id: int
    name: str


@dataclass(frozen=True)
class SimbaKingResponse:
    id: int
    name: str
