from pydantic import BaseModel, Field


class ShenziPackSchema(BaseModel):

    id: int = Field(0, description="Pack ID")
    name: str = Field("셴지 (Shenzi)", description="Pack leader's name")
    # 하이에나 무리를 통솔하는 전략적 리더. 스웜 기반 분산 스트레스 테스트 시나리오를 조율하는 부하 테스터

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 7,
                "name": "Shenzi",
            }
        }
    }
