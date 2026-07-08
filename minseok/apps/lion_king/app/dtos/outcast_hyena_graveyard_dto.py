from dataclasses import dataclass


@dataclass(frozen=True)
class HyenaGraveyardQuery:
    id: int
    name: str


@dataclass(frozen=True)
class HyenaGraveyardResponse:
    id: int
    name: str
