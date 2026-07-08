from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_homes.app.dtos.telegram_dto import TelegramResponse


class TelegramUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, component_id: int, name: str) -> TelegramResponse:
        '''텔레그램 인바운드 어댑터 컴포넌트의 자기소개 스켈레톤.'''
        ...
