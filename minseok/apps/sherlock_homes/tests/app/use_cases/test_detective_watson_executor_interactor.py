from unittest.mock import AsyncMock, patch

import pytest

from sherlock_homes.app.dtos.detective_watson_executor_dto import DispatchCommand
from sherlock_homes.app.use_cases.detective_watson_executor_interactor import WatsonExecutorInteractor


@pytest.mark.asyncio
async def test_dispatch_generates_subject_body_and_sends():
    port = AsyncMock()
    port.send.return_value = {"status": "ok"}

    interactor = WatsonExecutorInteractor(port=port)

    with patch(
        "sherlock_homes.app.use_cases.detective_watson_executor_interactor.orchestrator"
    ) as mock_orchestrator:
        # 1차 호출=본문, 2차 호출=제목
        mock_orchestrator.orchestrate = AsyncMock(side_effect=["본문 내용", "  제목  "])
        result = await interactor.dispatch(
            DispatchCommand(to_email="a@b.com", topic="회의 안내")
        )

    # 오케스트레이터를 본문·제목 각 1회씩 호출
    assert mock_orchestrator.orchestrate.await_count == 2
    # 주소록 미주입(port만) → name="", 제목은 strip 되어 포트로 전달
    port.send.assert_awaited_once_with("a@b.com", "제목", "본문 내용", name="")
    assert result.status == "sent"
