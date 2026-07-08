import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends

from sherlock_homes.adapter.inbound.api.schemas.detective_spam_classifier_schema import SpamClassifyRequest
from sherlock_homes.app.dtos.detective_spam_classifier_dto import ClassifyCommand, ClassifyResult
from sherlock_homes.app.ports.input.detective_spam_classifier_use_case import SpamClassifierUseCase
from sherlock_homes.dependencies.detective_spam_classifier_provider import get_spam_classifier_use_case

logger = logging.getLogger(__name__)

spam_classifier_router = APIRouter(prefix="/spam", tags=["spam"])


@spam_classifier_router.post("/classify")
async def classify_email(
    schema: Annotated[SpamClassifyRequest, Body()],
    classifier: SpamClassifierUseCase = Depends(get_spam_classifier_use_case),
) -> ClassifyResult:
    logger.info("[spam/classify] len=%d", len(schema.text))
    return await classifier.classify(ClassifyCommand(text=schema.text))
