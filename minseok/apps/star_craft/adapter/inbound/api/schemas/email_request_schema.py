from pydantic import BaseModel, EmailStr, Field


class EmailRequestSchema(BaseModel):
    to: EmailStr = Field(..., description="수신자 이메일 주소")
    content: str = Field(..., description="이메일에 담을 간단한 내용")

    model_config = {
        "json_schema_extra": {
            "example": {"to": "someone@example.com", "content": "다음 주 화요일 회의를 30분 미뤄도 될지 문의"}
        }
    }
