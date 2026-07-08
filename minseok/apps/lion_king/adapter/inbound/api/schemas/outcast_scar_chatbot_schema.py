from pydantic import BaseModel, Field


class ScarChatbotSchema(BaseModel):

    id: int = Field(0, description="Chatbot ID")
    name: str = Field("스카 (Scar)", description="Chatbot's name")
    # 교묘한 말로 무파사를 함정에 빠뜨린 자문 반역자. 조작적·적대적 입력 시나리오로 취약점을 탐지하는 레드팀

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 5,
                "name": "Scar",
            }
        }
    }
