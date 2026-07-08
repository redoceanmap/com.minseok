from __future__ import annotations

from star_craft.app.dtos.email_request_dto import EmailRequestCommand, EmailRequestResult
from star_craft.app.ports.input.email_request_use_case import EmailRequestUseCase
from star_craft.app.ports.output.email_composer_port import EmailComposerPort
from star_craft.domain.email.email_ontology import render_instruction


class EmailRequestInteractor(EmailRequestUseCase):

    def __init__(self, composer: EmailComposerPort) -> None:
        self._composer = composer

    async def request(self, command: EmailRequestCommand) -> EmailRequestResult:
        instruction = render_instruction(command.content)
        detail = await self._composer.compose_and_send(command.to_email, instruction)
        return EmailRequestResult(status="sent", detail=detail)
