from pydantic import BaseModel, Field


class NalaQueenSchema(BaseModel):

    id: int = Field(0, description="Queen ID")
    name: str = Field("날라 (Nala)", description="Queen's name")
    # 심바를 왕좌로 불러낸 왕비. 장기 전략 수립과 비즈니스 플래닝 데이터를 처리하는 전략 플래너

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 2,
                "name": "Nala",
            }
        }
    }
