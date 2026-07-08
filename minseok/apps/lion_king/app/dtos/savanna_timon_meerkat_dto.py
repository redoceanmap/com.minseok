from dataclasses import dataclass


@dataclass(frozen=True)
class TimonMeerkatQuery:
    id: int
    name: str


@dataclass(frozen=True)
class TimonMeerkatResponse:
    id: int
    name: str
