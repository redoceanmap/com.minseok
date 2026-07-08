from dataclasses import dataclass


@dataclass
class JusoQuery:
    id: int
    name: str


@dataclass
class JusoResponse:
    id: int
    name: str


@dataclass
class ContactCommand:
    name: str
    nickname: str
    email: str
    phone: str


@dataclass
class ContactView:
    id: int
    name: str
    nickname: str
    email: str
    phone: str
