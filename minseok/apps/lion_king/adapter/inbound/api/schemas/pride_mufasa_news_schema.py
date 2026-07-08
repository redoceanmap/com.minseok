from pydantic import BaseModel, Field


class MufasaNewsSchema(BaseModel):

    id: int = Field(0, description="News ID")
    name: str = Field("무파사 (Mufasa)", description="News broadcaster's name")
    # 별빛 속에서도 심바에게 메시지를 전하는 선왕. 시스템 전반의 이벤트와 상태 변경을 실시간 브로드캐스트

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 3,
                "name": "Mufasa",
            }
        }
    }
