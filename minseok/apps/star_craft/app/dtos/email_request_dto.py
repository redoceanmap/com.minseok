from dataclasses import dataclass

from pydantic import BaseModel


@dataclass(frozen=True)
class EmailRequestCommand:
    to_email: str
    content: str


class EmailRequestResult(BaseModel):
    status: str
    detail: str
