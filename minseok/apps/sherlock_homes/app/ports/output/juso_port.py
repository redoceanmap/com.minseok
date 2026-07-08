from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_homes.app.dtos.juso_dto import ContactCommand, ContactView, JusoQuery, JusoResponse


class JusoPort(ABC):

    @abstractmethod
    async def introduce_myself(self, query: JusoQuery) -> JusoResponse:
        '''주소록 관리인의 자기소개 레포지토리 추상 메소드'''
        ...

    @abstractmethod
    async def receive_uploaded_records(self, commands: list[ContactCommand]) -> int:
        '''정규화된 주소록 커맨드를 저장하고 저장 건수를 반환한다.'''
        ...

    @abstractmethod
    async def list_contacts(self) -> list[ContactView]:
        '''저장된 주소록 전체를 조회한다.'''
        ...
