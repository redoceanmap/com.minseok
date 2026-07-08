from pydantic import BaseModel, Field


class SarabiGuardianSchema(BaseModel):

    id: int = Field(0, description="Guardian ID")
    name: str = Field("사라비 (Sarabi)", description="Guardian's name")
    # 스카의 압제 속에서도 프라이드 록의 가치를 지켜낸 심바의 어머니. 도메인 헤리티지 데이터 보호 및 복원 로직

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 4,
                "name": "Sarabi",
            }
        }
    }
