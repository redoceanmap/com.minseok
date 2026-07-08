from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_homes.app.dtos.detective_spam_classifier_dto import ClassifyCommand, ClassifyResult


class SpamClassifierUseCase(ABC):

    @abstractmethod
    async def classify(self, command: ClassifyCommand) -> ClassifyResult:
        '''이메일 텍스트를 스팸 온톨로지(허브)에 따라 LLM으로 분류한다.'''
        ...
