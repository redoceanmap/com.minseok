from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_homes.app.dtos.inbound_mail_dto import InboundMailCommand, InboundMailView


class InboundMailPort(ABC):

    @abstractmethod
    async def save(self, command: InboundMailCommand) -> bool:
        '''수신 메일을 저장한다(message_id 중복은 무시). 신규 저장 True, 중복 False.'''
        ...

    @abstractmethod
    async def list_recent(self) -> list[InboundMailView]:
        '''저장된 수신 메일을 최신순으로 반환한다.'''
        ...
