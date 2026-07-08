from fastapi import APIRouter, Depends

from sherlock_homes.adapter.inbound.api.schemas.discord_schema import DiscordIntroduceResponse
from sherlock_homes.app.ports.input.discord_use_case import DiscordUseCase
from sherlock_homes.dependencies.discord_provider import get_discord_use_case

'''
 discord_router.py — 디스코드 연동 인바운드 어댑터 (스켈레톤)
'''
discord_router = APIRouter(prefix="/discord", tags=["discord"])


@discord_router.get("/myself", response_model=DiscordIntroduceResponse)
async def introduce_myself(
    discord: DiscordUseCase = Depends(get_discord_use_case),
):
    return await discord.introduce_myself(component_id=1, name="디스코드 어댑터")
