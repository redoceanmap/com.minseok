from dataclasses import dataclass


@dataclass(frozen=True)
class ScarChatbotQuery:
    id: int
    name: str


@dataclass(frozen=True)
class ScarChatbotResponse:
    id: int
    name: str
