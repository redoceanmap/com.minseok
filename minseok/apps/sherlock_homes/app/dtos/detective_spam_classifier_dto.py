from dataclasses import dataclass

from pydantic import BaseModel

from star_craft.domain.spam.spam_category import SpamCategory


@dataclass(frozen=True)
class ClassifyCommand:
    text: str


class ClassifyResult(BaseModel):
    category: SpamCategory
