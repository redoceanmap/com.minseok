from pydantic import BaseModel, Field


class InboundMailRequestSchema(BaseModel):
    """n8n(Gmail Push 파이프라인)이 보내는 수신 메일 페이로드."""

    message_id: str = Field(..., alias="messageId", description="Gmail 메일 고유 ID")
    subject: str = Field("", description="제목")
    sender: str = Field("", alias="from", description="발신자")
    recipient: str = Field("", alias="to", description="수신자")
    preview: str = Field("", description="본문 미리보기(snippet)")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "subject": "한강라면 꿀팁 레시피 전달",
                "from": '"장민석" <jang971121@gmail.com>',
                "to": "jang971121@gmail.com",
                "preview": "안녕하세요, 친구님! 오늘은...",
                "messageId": "19f1bd7f5cd1d09b",
            }
        },
    }


class InboundMailResultSchema(BaseModel):
    saved: bool = Field(..., description="신규 저장 여부(중복이면 False)")
    message_id: str = Field(..., description="저장 시도한 메일 ID")


class InboundMailItemSchema(BaseModel):
    id: int = Field(..., description="레코드 ID")
    message_id: str = Field(..., description="Gmail 메일 고유 ID")
    subject: str = Field("", description="제목")
    sender: str = Field("", description="발신자")
    recipient: str = Field("", description="수신자")
    preview: str = Field("", description="본문 미리보기")
    received_at: str = Field("", description="수신 저장 시각(ISO)")
