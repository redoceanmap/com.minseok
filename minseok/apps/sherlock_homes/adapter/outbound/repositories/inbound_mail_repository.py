from __future__ import annotations

import logging

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from sherlock_homes.adapter.outbound.mappers.inbound_mail_mapper import InboundMailMapper
from sherlock_homes.adapter.outbound.orm.inbound_mail_orm import InboundMailOrm
from sherlock_homes.app.dtos.inbound_mail_dto import InboundMailCommand, InboundMailView
from sherlock_homes.app.ports.output.inbound_mail_port import InboundMailPort

logger = logging.getLogger(__name__)


class InboundMailRepository(InboundMailPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, command: InboundMailCommand) -> bool:
        # message_id 가 고유키 → 같은 메일이 중복 push 되어도 한 번만 저장 (dedup)
        stmt = (
            pg_insert(InboundMailOrm)
            .values(
                message_id=command.message_id,
                subject=command.subject,
                sender=command.sender,
                recipient=command.recipient,
                preview=command.preview,
            )
            .on_conflict_do_nothing(index_elements=["message_id"])
            .returning(InboundMailOrm.id)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        # RETURNING 은 실제 삽입된 행만 반환 → 충돌(중복)이면 빈 결과
        saved = result.first() is not None
        logger.info(
            f"[InboundMailRepository] save | message_id={command.message_id} saved={saved}"
        )
        return saved

    async def list_recent(self) -> list[InboundMailView]:
        result = await self.session.execute(
            select(InboundMailOrm).order_by(InboundMailOrm.id.desc())
        )
        return [InboundMailMapper.to_view(orm) for orm in result.scalars().all()]
