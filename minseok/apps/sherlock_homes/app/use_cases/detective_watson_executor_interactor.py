from __future__ import annotations

from core.lol.t1_mid_faker_orchestrator import EXAONE_2_4B, orchestrator
from sherlock_homes.app.dtos.detective_watson_executor_dto import DispatchCommand, DispatchResult
from sherlock_homes.app.ports.input.detective_watson_executor_use_case import WatsonExecutorUseCase
from sherlock_homes.app.ports.output.detective_watson_executor_directory_port import ContactDirectoryPort
from sherlock_homes.app.ports.output.detective_watson_executor_port import WatsonExecutorPort


class WatsonExecutorInteractor(WatsonExecutorUseCase):

    def __init__(
        self,
        port: WatsonExecutorPort,
        directory: ContactDirectoryPort | None = None,
    ) -> None:
        self._port = port
        self._directory = directory

    async def dispatch(self, command: DispatchCommand) -> DispatchResult:
        # 받는 사람 이름을 주소록에서 조회 (없으면 빈 문자열 → n8n이 이메일로 폴백)
        name = ""
        if self._directory is not None:
            name = await self._directory.find_name_by_email(command.to_email)

        body = await orchestrator.orchestrate(
            f"다음 주제로 이메일 본문을 한국어로 작성해줘. 인사말과 맺음말을 포함해. 주제: {command.topic}",
            model=EXAONE_2_4B,
        )
        subject = await orchestrator.orchestrate(
            f"다음 이메일 본문에 어울리는 제목을 따옴표 없이 한 줄로만 작성해줘:\n\n{body}",
            model=EXAONE_2_4B,
        )
        result = await self._port.send(command.to_email, subject.strip(), body, name=name)
        return DispatchResult(status="sent", detail=str(result))
