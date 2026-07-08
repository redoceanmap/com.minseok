from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_homes.app.dtos.inbound_mail_dto import InboundMailCommand, InboundMailView


class InboundMailUseCase(ABC):

    @abstractmethod
    async def receive_mail(self, command: InboundMailCommand) -> bool:
        '''n8n(Gmail Push)에서 받은 수신 메일을 저장한다. 신규 저장이면 True, 중복이면 False.'''
        ...

    @abstractmethod
    async def list_mails(self) -> list[InboundMailView]:
        '''저장된 수신 메일을 최신순으로 조회한다.'''
        ...
