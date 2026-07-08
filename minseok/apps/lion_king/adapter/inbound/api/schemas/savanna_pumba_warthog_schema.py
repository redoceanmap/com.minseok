from pydantic import BaseModel, Field


class PumbaWarthogSchema(BaseModel):

    id: int = Field(0, description="Warthog ID")
    name: str = Field("품바 (Pumba)", description="Warthog's name")
    # 무거운 짐도 마다않고 돌진하는 혹멧돼지. 대용량 배치 데이터를 비동기로 처리하는 배치 프로세서

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 11,
                "name": "Pumba",
            }
        }
    }
