from dataclasses import dataclass
from pydantic import BaseModel


@dataclass(frozen=True)
class SmithCaptainQuery:
    id: int
    name: str


@dataclass(frozen=True)
class SmithCaptainResponse:
    id: int
    name: str


class ChatResponse(BaseModel):
    text: str


class ReportSummaryResponse(BaseModel):
    generated_at: str
    total_passengers: int
    total_survivors: int
    survival_rate: float
    male_survival_rate: float
    female_survival_rate: float
    class_1_survival_rate: float
    class_2_survival_rate: float
    class_3_survival_rate: float
    avg_age: float
 