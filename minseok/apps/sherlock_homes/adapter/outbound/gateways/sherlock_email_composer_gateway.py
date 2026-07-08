from __future__ import annotations

from sherlock_homes.adapter.outbound.gateways.detective_watson_executor_n8n_gateway import WatsonExecutorN8nGateway
from sherlock_homes.app.dtos.detective_watson_executor_dto import DispatchCommand
from sherlock_homes.app.use_cases.detective_watson_executor_interactor import WatsonExecutorInteractor
from star_craft.app.ports.output.email_composer_port import EmailComposerPort


class SherlockEmailComposerGateway(EmailComposerPort):
    '''허브의 EmailComposerPort를 셜록(스포크)이 구현한다.

    스포크 → 허브 추상에만 의존(스타 토폴로지 허용). 어제 완성된 watson 파이프라인
    (2.4b 작성 + n8n/Gmail 발송)을 그대로 재사용하며, 허브의 온톨로지 지시(instruction)를
    watson의 topic으로 전달한다.
    '''

    def __init__(self) -> None:
        self._watson = WatsonExecutorInteractor(port=WatsonExecutorN8nGateway())

    async def compose_and_send(self, to_email: str, instruction: str) -> str:
        result = await self._watson.dispatch(DispatchCommand(to_email=to_email, topic=instruction))
        return result.detail
