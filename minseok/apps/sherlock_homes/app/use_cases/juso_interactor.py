from __future__ import annotations

from sherlock_homes.app.dtos.juso_dto import ContactCommand, ContactView, JusoQuery, JusoResponse
from sherlock_homes.app.ports.input.juso_use_case import JusoUseCase
from sherlock_homes.app.ports.output.juso_port import JusoPort


class JusoInteractor(JusoUseCase):
    def __init__(self, repository: JusoPort) -> None:
        self.repository = repository

    async def introduce_myself(self, juso_id: int, name: str) -> JusoResponse:
        '''221B 주소록 관리인의 자기소개 인터랙터'''
        return await self.repository.introduce_myself(JusoQuery(id=juso_id, name=name))

    async def upload_contacts(self, commands: list[ContactCommand]) -> dict:
        saved = await self.repository.receive_uploaded_records(commands)
        return {"saved": saved}

    async def list_contacts(self) -> list[ContactView]:
        return await self.repository.list_contacts()
