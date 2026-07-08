from dataclasses import dataclass


@dataclass(frozen=True)
class SarabiGuardianQuery:
    id: int
    name: str


@dataclass(frozen=True)
class SarabiGuardianResponse:
    id: int
    name: str
