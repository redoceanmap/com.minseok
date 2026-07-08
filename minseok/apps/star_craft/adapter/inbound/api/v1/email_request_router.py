import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends

from star_craft.adapter.inbound.api.schemas.email_request_schema import EmailRequestSchema
from star_craft.app.dtos.email_request_dto import EmailRequestCommand, EmailRequestResult
from star_craft.app.ports.input.email_request_use_case import EmailRequestUseCase
from star_craft.dependencies.email_request_provider import get_email_request_use_case

logger = logging.getLogger(__name__)

email_request_router = APIRouter(prefix="/email", tags=["star_craft-email"])


@email_request_router.post("/request")
async def request_email(
    schema: Annotated[EmailRequestSchema, Body()],
    use_case: EmailRequestUseCase = Depends(get_email_request_use_case),
) -> EmailRequestResult:
    logger.info("[star_craft/email/request] to=%s", schema.to)
    return await use_case.request(EmailRequestCommand(to_email=schema.to, content=schema.content))
