from pydantic import BaseModel, Field


class SimbaKingSchema(BaseModel):

    id: int = Field(0, description="King ID")
    name: str = Field("심바 (Simba)", description="King's name")
    # 프라이드 록의 왕으로 귀환한 심바. 전체 에이전트 워크플로우를 조율하는 중앙 오케스트레이터

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Simba",
            }
        }
    }
