from __future__ import annotations

import logging

from sherlock_homes.app.dtos.telegram_dto import TelegramQuery, TelegramResponse
from sherlock_homes.app.ports.output.telegram_port import TelegramPort

logger = logging.getLogger(__name__)


class TelegramRepository(TelegramPort):

    async def introduce_myself(self, query: TelegramQuery) -> TelegramResponse:
        logger.info(f"[TelegramRepository] introduce_myself 진입 | query={query}")
        return TelegramResponse(id=query.id, name=query.name)
