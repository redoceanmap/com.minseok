from pydantic import BaseModel, EmailStr, Field


class EmailDispatchRequest(BaseModel):
    to: EmailStr = Field(..., description="수신자 이메일 주소")
    topic: str = Field(..., description="이메일 작성 주제")

    model_config = {
        "json_schema_extra": {
            "example": {"to": "someone@example.com", "topic": "다음 주 팀 회의 일정 안내"}
        }
    }
