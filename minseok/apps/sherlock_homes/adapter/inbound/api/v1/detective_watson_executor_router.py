import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends

from sherlock_homes.adapter.inbound.api.schemas.detective_watson_executor_schema import EmailDispatchRequest
from sherlock_homes.app.dtos.detective_watson_executor_dto import DispatchCommand, DispatchResult
from sherlock_homes.app.ports.input.detective_watson_executor_use_case import WatsonExecutorUseCase
from sherlock_homes.dependencies.detective_watson_executor_provider import get_watson_executor_use_case

logger = logging.getLogger(__name__)

watson_executor_router = APIRouter(prefix="/watson", tags=["watson"])


@watson_executor_router.post("/email/dispatch")
async def dispatch_email(
    schema: Annotated[EmailDispatchRequest, Body()],
    watson: WatsonExecutorUseCase = Depends(get_watson_executor_use_case),
) -> DispatchResult:
    logger.info("[watson/email/dispatch] to=%s topic=%s", schema.to, schema.topic)
    return await watson.dispatch(DispatchCommand(to_email=schema.to, topic=schema.topic))
