from pydantic import BaseModel, Field


class TelegramIntroduceResponse(BaseModel):
    '''/telegram/myself 응답 스켈레톤.'''

    id: int = Field(..., description="컴포넌트 ID")
    name: str = Field(..., description="컴포넌트 이름")
