from fastapi import APIRouter, Depends

from sherlock_homes.adapter.inbound.api.schemas.inbound_mail_schema import (
    InboundMailItemSchema,
    InboundMailRequestSchema,
    InboundMailResultSchema,
)
from sherlock_homes.app.dtos.inbound_mail_dto import InboundMailCommand
from sherlock_homes.app.ports.input.inbound_mail_use_case import InboundMailUseCase
from sherlock_homes.dependencies.inbound_mail_provider import get_inbound_mail_use_case

'''
inbound_mail_router.py — Gmail Push(n8n) 수신 메일 인바운드 어댑터.
n8n HTTP Request 노드가 POST /api/sherlock/mail/inbound 로 메일을 보낸다. (webhook.site 대체)
'''
inbound_mail_router = APIRouter(prefix="/mail", tags=["inbound-mail"])


@inbound_mail_router.post(
    "/inbound", response_model=InboundMailResultSchema, summary="n8n 수신 메일 저장"
)
async def receive_inbound_mail(
    payload: InboundMailRequestSchema,
    mail: InboundMailUseCase = Depends(get_inbound_mail_use_case),
):
    saved = await mail.receive_mail(
        InboundMailCommand(
            message_id=payload.message_id,
            subject=payload.subject,
            sender=payload.sender,
            recipient=payload.recipient,
            preview=payload.preview,
        )
    )
    return InboundMailResultSchema(saved=saved, message_id=payload.message_id)


@inbound_mail_router.get(
    "/list", response_model=list[InboundMailItemSchema], summary="수신 메일 목록 조회"
)
async def list_inbound_mails(
    mail: InboundMailUseCase = Depends(get_inbound_mail_use_case),
):
    views = await mail.list_mails()
    return [
        InboundMailItemSchema(
            id=v.id,
            message_id=v.message_id,
            subject=v.subject,
            sender=v.sender,
            recipient=v.recipient,
            preview=v.preview,
            received_at=v.received_at,
        )
        for v in views
    ]
