from pydantic import BaseModel, Field


class AncestorsStarsSchema(BaseModel):

    id: int = Field(0, description="Stars ID")
    name: str = Field("선조들 (Ancestors)", description="Ancestors' name")
    # 스카의 통치로 잊혀진 왕들의 별빛. 시스템 이상 시 과거 정상 패턴 기반 이상 탐지 및 롤백 기준점 제공

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 8,
                "name": "Ancestors",
            }
        }
    }
