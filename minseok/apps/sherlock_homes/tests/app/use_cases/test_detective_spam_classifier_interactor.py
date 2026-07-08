from unittest.mock import AsyncMock

import pytest

from sherlock_homes.app.dtos.detective_spam_classifier_dto import ClassifyCommand
from sherlock_homes.app.ports.output.detective_spam_classifier_port import SpamClassifierPort
from sherlock_homes.app.use_cases.detective_spam_classifier_interactor import SpamClassifierInteractor
from star_craft.domain.spam.spam_category import SpamCategory


@pytest.mark.asyncio
async def test_classify_maps_llm_answer_to_category():
    port = AsyncMock(spec=SpamClassifierPort)
    port.classify = AsyncMock(return_value="phishing")
    interactor = SpamClassifierInteractor(port=port)

    result = await interactor.classify(ClassifyCommand(text="계정 확인이 필요합니다 login now"))

    assert result.category == SpamCategory.PHISHING


@pytest.mark.asyncio
async def test_classify_defaults_to_legitimate_on_unknown_answer():
    port = AsyncMock(spec=SpamClassifierPort)
    port.classify = AsyncMock(return_value="잘 모르겠습니다")
    interactor = SpamClassifierInteractor(port=port)

    result = await interactor.classify(ClassifyCommand(text="내일 점심 같이 먹어요"))

    assert result.category == SpamCategory.LEGITIMATE
