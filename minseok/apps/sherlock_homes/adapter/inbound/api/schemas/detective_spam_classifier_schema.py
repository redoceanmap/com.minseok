from pydantic import BaseModel, Field


class SpamClassifyRequest(BaseModel):
    text: str = Field(..., description="분류할 이메일 본문")

    model_config = {
        "json_schema_extra": {
            "example": {"text": "계정 확인이 필요합니다. 지금 login 하세요."}
        }
    }
