from __future__ import annotations

import logging

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from sherlock_homes.adapter.outbound.mappers.juso_mapper import JusoMapper
from sherlock_homes.adapter.outbound.orm.juso_orm import JusoOrm
from sherlock_homes.app.dtos.juso_dto import ContactCommand, ContactView, JusoQuery, JusoResponse
from sherlock_homes.app.ports.output.juso_port import JusoPort

logger = logging.getLogger(__name__)


class JusoRepository(JusoPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: JusoQuery) -> JusoResponse:
        logger.info(f"[JusoRepository] introduce_myself 진입 | query={query}")
        return JusoResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴",
        )

    async def receive_uploaded_records(self, commands: list[ContactCommand]) -> int:
        # 이메일이 고유키 → 이메일 없는 레코드 제외 + 같은 CSV 내 이메일 중복은 마지막 값으로 dedup
        by_email: dict[str, dict] = {}
        for cmd in commands:
            email = cmd.email.strip()
            if not email:
                continue
            by_email[email] = {
                "email": email,
                "name": cmd.name,
                "nickname": cmd.nickname,
                "phone": cmd.phone,
            }

        values = list(by_email.values())
        if not values:
            return 0

        stmt = pg_insert(JusoOrm).values(values)
        stmt = stmt.on_conflict_do_update(
            index_elements=["email"],
            set_={
                "name": stmt.excluded.name,
                "nickname": stmt.excluded.nickname,
                "phone": stmt.excluded.phone,
            },
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"[JusoRepository] receive_uploaded_records | saved={len(values)}")
        return len(values)

    async def list_contacts(self) -> list[ContactView]:
        result = await self.session.execute(select(JusoOrm).order_by(JusoOrm.id))
        return [JusoMapper.to_view(orm) for orm in result.scalars().all()]
