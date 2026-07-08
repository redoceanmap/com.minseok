from __future__ import annotations

from abc import ABC, abstractmethod


class SpamClassifierPort(ABC):

    @abstractmethod
    async def classify(self, prompt: str) -> str:
        '''완성된 프롬프트를 LLM에 전달하고 모델의 원문 응답을 반환한다.'''
        ...
