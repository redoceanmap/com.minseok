from pydantic import BaseModel, Field


class RafikiFaqSchema(BaseModel):

    id: int = Field(0, description="FAQ ID")
    name: str = Field("라피키 (Rafiki)", description="FAQ keeper's name")
    # 수수께끼 같은 지혜로 사바나를 누비며 심바를 인도하는 만드릴. 반복 질의 지식을 구조화하는 FAQ 지식 베이스

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 12,
                "name": "Rafiki",
            }
        }
    }
