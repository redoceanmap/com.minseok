from dataclasses import dataclass


@dataclass(frozen=True)
class PumbaWarthogQuery:
    id: int
    name: str


@dataclass(frozen=True)
class PumbaWarthogResponse:
    id: int
    name: str
