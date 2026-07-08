from dataclasses import dataclass


@dataclass
class DiscordQuery:
    id: int
    name: str


@dataclass
class DiscordResponse:
    id: int
    name: str
