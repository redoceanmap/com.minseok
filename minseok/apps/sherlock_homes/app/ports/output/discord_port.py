from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_homes.app.dtos.discord_dto import DiscordQuery, DiscordResponse


class DiscordPort(ABC):

    @abstractmethod
    async def introduce_myself(self, query: DiscordQuery) -> DiscordResponse:
        '''디스코드 컴포넌트의 자기소개 레포지토리 추상 메소드.'''
        ...
