from io import StringIO
import csv

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from sherlock_homes.adapter.inbound.api.schemas.juso_schema import (
    ContactItemSchema,
    ContactUploadSchema,
    UploadResultSchema,
)
from sherlock_homes.app.dtos.juso_dto import ContactCommand
from sherlock_homes.app.ports.input.juso_use_case import JusoUseCase
from sherlock_homes.dependencies.juso_provider import get_juso_use_case

'''
 juso_router.py
 CSV → ContactCommand 변환은 어댑터(이 라우터)가 담당하고,
 유스케이스에는 DTO(ContactCommand)만 넘긴다. (app → adapter 의존 차단)
'''
juso_router = APIRouter(prefix="/juso", tags=["juso"])


@juso_router.get("/myself")
async def introduce_myself(
    juso: JusoUseCase = Depends(get_juso_use_case),
):
    return await juso.introduce_myself(juso_id=1, name="주소 어댑터")


@juso_router.post("/upload", response_model=UploadResultSchema, summary="구글 주소록 CSV 파일 업로드")
async def upload_contacts_file(
    file: UploadFile = File(...),
    juso: JusoUseCase = Depends(get_juso_use_case),
):
    text = (await file.read()).decode("utf-8-sig", errors="replace")
    return await juso.upload_contacts(_parse_csv(text))


@juso_router.get("/contacts", response_model=list[ContactItemSchema], summary="저장된 주소록 목록 조회")
async def list_contacts(
    juso: JusoUseCase = Depends(get_juso_use_case),
):
    views = await juso.list_contacts()
    return [
        ContactItemSchema(
            id=v.id, name=v.name, nickname=v.nickname, email=v.email, phone=v.phone
        )
        for v in views
    ]


# 구글 주소록 CSV 헤더 → ContactUploadSchema 필드 매핑 (그 외 열은 무시)
_CONTACT_FIELD_MAP = {
    "first name": "first_name",
    "last name": "last_name",
    "nickname": "nickname",
    "e-mail 1 - value": "email",
    "phone 1 - value": "phone",
}


def _parse_csv(text: str) -> list[ContactCommand]:
    if not text.strip():
        raise HTTPException(status_code=400, detail="빈 CSV 파일입니다.")
    reader = csv.DictReader(StringIO(text))
    if reader.fieldnames is None:
        raise HTTPException(status_code=400, detail="CSV 헤더를 읽을 수 없습니다.")
    return [
        _to_command(ContactUploadSchema(**_normalize_contact_row(row)))
        for row in reader
    ]


def _to_command(record: ContactUploadSchema) -> ContactCommand:
    return ContactCommand(
        name=_display_name(record),
        nickname=record.nickname or "",
        email=record.email or "",
        phone=record.phone or "",
    )


def _display_name(record: ContactUploadSchema) -> str:
    parts = [record.first_name, record.last_name]
    name = " ".join(p.strip() for p in parts if p and p.strip())
    return name or (record.nickname or "")


def _normalize_contact_row(row: dict) -> dict:
    normalized = {}
    for raw_key, value in row.items():
        if raw_key is None:
            continue
        field = _CONTACT_FIELD_MAP.get(raw_key.strip().lower())
        if field:
            normalized[field] = value
    return normalized
