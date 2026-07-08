from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_homes.app.dtos.telegram_dto import TelegramQuery, TelegramResponse


class TelegramPort(ABC):

    @abstractmethod
    async def introduce_myself(self, query: TelegramQuery) -> TelegramResponse:
        '''텔레그램 컴포넌트의 자기소개 레포지토리 추상 메소드.'''
        ...
