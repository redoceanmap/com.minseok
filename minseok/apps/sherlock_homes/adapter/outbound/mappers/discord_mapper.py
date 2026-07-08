from __future__ import annotations

from sherlock_homes.adapter.outbound.orm.discord_orm import DiscordOrm
from sherlock_homes.app.dtos.discord_dto import DiscordResponse


class DiscordMapper:

    @staticmethod
    def to_response(orm: DiscordOrm) -> DiscordResponse:
        return DiscordResponse(id=orm.id, name=orm.name or "")
