from dataclasses import dataclass


@dataclass
class TelegramQuery:
    id: int
    name: str


@dataclass
class TelegramResponse:
    id: int
    name: str
