from dataclasses import dataclass


@dataclass
class InboundMailCommand:
    message_id: str
    subject: str
    sender: str
    recipient: str
    preview: str


@dataclass
class InboundMailView:
    id: int
    message_id: str
    subject: str
    sender: str
    recipient: str
    preview: str
    received_at: str
