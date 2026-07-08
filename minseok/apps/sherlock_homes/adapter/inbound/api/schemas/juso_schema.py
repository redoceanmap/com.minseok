from typing import Optional

from pydantic import BaseModel, Field


class ContactUploadSchema(BaseModel):
    """구글 주소록 CSV 한 행에서 주소록에 필요한 필드만 정규화한 스키마."""

    first_name: Optional[str] = Field(None, description="이름 (CSV: First Name)")
    last_name: Optional[str] = Field(None, description="성 (CSV: Last Name)")
    nickname: Optional[str] = Field(None, description="닉네임 (CSV: Nickname)")
    email: Optional[str] = Field(None, description="이메일 (CSV: E-mail 1 - Value)")
    phone: Optional[str] = Field(None, description="전화번호 (CSV: Phone 1 - Value)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "왓슨",
                "last_name": "존",
                "nickname": "왓슨",
                "email": "john.watson@example.com",
                "phone": "010-1234-5678",
            }
        }
    }


class UploadResultSchema(BaseModel):
    saved: int = Field(..., description="저장된 주소록 레코드 수")


class ContactItemSchema(BaseModel):
    id: int = Field(..., description="주소록 레코드 ID")
    name: str = Field("", description="이름")
    nickname: str = Field("", description="닉네임")
    email: str = Field(..., description="이메일")
    phone: str = Field("", description="전화번호")
