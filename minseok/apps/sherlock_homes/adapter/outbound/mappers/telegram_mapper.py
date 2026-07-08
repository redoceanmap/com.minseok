from __future__ import annotations

from sherlock_homes.adapter.outbound.orm.telegram_orm import TelegramOrm
from sherlock_homes.app.dtos.telegram_dto import TelegramResponse


class TelegramMapper:

    @staticmethod
    def to_response(orm: TelegramOrm) -> TelegramResponse:
        return TelegramResponse(id=orm.id, name=orm.name or "")
