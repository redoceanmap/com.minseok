from __future__ import annotations

from sherlock_homes.app.dtos.discord_dto import DiscordQuery, DiscordResponse
from sherlock_homes.app.ports.input.discord_use_case import DiscordUseCase
from sherlock_homes.app.ports.output.discord_port import DiscordPort


class DiscordInteractor(DiscordUseCase):
    def __init__(self, repository: DiscordPort) -> None:
        self.repository = repository

    async def introduce_myself(self, component_id: int, name: str) -> DiscordResponse:
        return await self.repository.introduce_myself(
            DiscordQuery(id=component_id, name=name)
        )
