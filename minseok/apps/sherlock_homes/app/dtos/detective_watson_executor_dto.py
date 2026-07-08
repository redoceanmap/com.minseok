from dataclasses import dataclass

from pydantic import BaseModel


@dataclass(frozen=True)
class DispatchCommand:
    to_email: str
    topic: str


class DispatchResult(BaseModel):
    status: str
    detail: str
