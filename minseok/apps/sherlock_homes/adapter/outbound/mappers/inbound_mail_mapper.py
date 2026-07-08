from __future__ import annotations

from sherlock_homes.adapter.outbound.orm.inbound_mail_orm import InboundMailOrm
from sherlock_homes.app.dtos.inbound_mail_dto import InboundMailView


class InboundMailMapper:

    @staticmethod
    def to_view(orm: InboundMailOrm) -> InboundMailView:
        return InboundMailView(
            id=orm.id,
            message_id=orm.message_id,
            subject=orm.subject or "",
            sender=orm.sender or "",
            recipient=orm.recipient or "",
            preview=orm.preview or "",
            received_at=orm.received_at.isoformat() if orm.received_at else "",
        )
