from __future__ import annotations

from sherlock_homes.app.dtos.inbound_mail_dto import InboundMailCommand, InboundMailView
from sherlock_homes.app.ports.input.inbound_mail_use_case import InboundMailUseCase
from sherlock_homes.app.ports.output.inbound_mail_port import InboundMailPort


class InboundMailInteractor(InboundMailUseCase):
    def __init__(self, repository: InboundMailPort) -> None:
        self.repository = repository

    async def receive_mail(self, command: InboundMailCommand) -> bool:
        return await self.repository.save(command)

    async def list_mails(self) -> list[InboundMailView]:
        return await self.repository.list_recent()
