from __future__ import annotations

from sherlock_homes.app.dtos.telegram_dto import TelegramQuery, TelegramResponse
from sherlock_homes.app.ports.input.telegram_use_case import TelegramUseCase
from sherlock_homes.app.ports.output.telegram_port import TelegramPort


class TelegramInteractor(TelegramUseCase):
    def __init__(self, repository: TelegramPort) -> None:
        self.repository = repository

    async def introduce_myself(self, component_id: int, name: str) -> TelegramResponse:
        return await self.repository.introduce_myself(
            TelegramQuery(id=component_id, name=name)
        )
