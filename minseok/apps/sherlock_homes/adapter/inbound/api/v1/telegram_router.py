from fastapi import APIRouter, Depends

from sherlock_homes.adapter.inbound.api.schemas.telegram_schema import TelegramIntroduceResponse
from sherlock_homes.app.ports.input.telegram_use_case import TelegramUseCase
from sherlock_homes.dependencies.telegram_provider import get_telegram_use_case

'''
telegram_router.py — 텔레그램 연동 인바운드 어댑터 (스켈레톤)
'''
telegram_router = APIRouter(prefix="/telegram", tags=["telegram"])


@telegram_router.get("/myself", response_model=TelegramIntroduceResponse)
async def introduce_myself(
    telegram: TelegramUseCase = Depends(get_telegram_use_case),
):
    return await telegram.introduce_myself(component_id=1, name="텔레그램 어댑터")
