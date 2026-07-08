from __future__ import annotations

from sherlock_homes.app.dtos.detective_spam_classifier_dto import ClassifyCommand, ClassifyResult
from sherlock_homes.app.ports.input.detective_spam_classifier_use_case import SpamClassifierUseCase
from sherlock_homes.app.ports.output.detective_spam_classifier_port import SpamClassifierPort
from star_craft.domain.spam.spam_category import SpamCategory

_LABELS = ", ".join(c.value for c in SpamCategory)


class SpamClassifierInteractor(SpamClassifierUseCase):

    def __init__(self, port: SpamClassifierPort) -> None:
        self._port = port

    async def classify(self, command: ClassifyCommand) -> ClassifyResult:
        answer = await self._port.classify(
            f"다음 이메일을 [{_LABELS}] 중 하나로 분류해. "
            f"설명 없이 카테고리 단어 하나만 답해.\n\n{command.text}"
        )
        return ClassifyResult(category=_parse_category(answer))


def _parse_category(answer: str) -> SpamCategory:
    '''LLM 응답에서 SpamCategory를 추출한다. 매칭 실패 시 LEGITIMATE.'''
    lowered = answer.lower()
    for category in SpamCategory:
        if category.value in lowered:
            return category
    return SpamCategory.LEGITIMATE
