from __future__ import annotations

from sherlock_homes.adapter.outbound.orm.juso_orm import JusoOrm
from sherlock_homes.app.dtos.juso_dto import ContactView


class JusoMapper:

    @staticmethod
    def to_view(orm: JusoOrm) -> ContactView:
        return ContactView(
            id=orm.id,
            name=orm.name or "",
            nickname=orm.nickname or "",
            email=orm.email,
            phone=orm.phone or "",
        )
