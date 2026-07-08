from pydantic import BaseModel, Field


class HyenaGraveyardSchema(BaseModel):

    id: int = Field(0, description="Graveyard ID")
    name: str = Field("하이에나 무리 (Hyenas)", description="Graveyard's name")
    # 코끼리 무덤에 서식하며 스카를 추종하는 무리. 처리 실패한 메시지와 예외 데이터를 수집하는 데드레터 큐

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 6,
                "name": "Hyenas",
            }
        }
    }
