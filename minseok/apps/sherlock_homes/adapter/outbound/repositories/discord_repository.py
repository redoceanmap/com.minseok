from __future__ import annotations

import logging

from sherlock_homes.app.dtos.discord_dto import DiscordQuery, DiscordResponse
from sherlock_homes.app.ports.output.discord_port import DiscordPort

logger = logging.getLogger(__name__)


class DiscordRepository(DiscordPort):

    async def introduce_myself(self, query: DiscordQuery) -> DiscordResponse:
        logger.info(f"[DiscordRepository] introduce_myself 진입 | query={query}")
        return DiscordResponse(id=query.id, name=query.name)
