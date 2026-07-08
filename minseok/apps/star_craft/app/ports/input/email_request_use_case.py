from __future__ import annotations

from abc import ABC, abstractmethod

from star_craft.app.dtos.email_request_dto import EmailRequestCommand, EmailRequestResult


class EmailRequestUseCase(ABC):

    @abstractmethod
    async def request(self, command: EmailRequestCommand) -> EmailRequestResult:
        '''프론트의 이메일 작성 요청을 받아 온톨로지 지시를 붙여 스포크에 위임한다.'''
        ...
