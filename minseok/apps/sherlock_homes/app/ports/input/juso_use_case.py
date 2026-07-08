from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_homes.app.dtos.juso_dto import ContactCommand, ContactView, JusoResponse


class JusoUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, juso_id: int, name: str) -> JusoResponse:
        '''221B 주소록 관리인의 자기소개 메소드'''
        ...

    @abstractmethod
    async def upload_contacts(self, commands: list[ContactCommand]) -> dict:
        '''정규화된 주소록 커맨드를 받아 저장한다.'''
        ...

    @abstractmethod
    async def list_contacts(self) -> list[ContactView]:
        '''저장된 주소록 전체를 조회한다.'''
        ...
