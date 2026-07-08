from dataclasses import dataclass


@dataclass(frozen=True)
class ShenziPackQuery:
    id: int
    name: str


@dataclass(frozen=True)
class ShenziPackResponse:
    id: int
    name: str
