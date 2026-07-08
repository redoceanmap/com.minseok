from unittest.mock import AsyncMock

import pytest

from star_craft.app.dtos.email_request_dto import EmailRequestCommand
from star_craft.app.use_cases.email_request_interactor import EmailRequestInteractor


@pytest.mark.asyncio
async def test_request_injects_ontology_and_delegates_to_composer():
    composer = AsyncMock()
    composer.compose_and_send.return_value = "sent"

    interactor = EmailRequestInteractor(composer=composer)
    result = await interactor.request(
        EmailRequestCommand(to_email="a@b.com", content="회의 일정 변경 문의")
    )

    # 스포크에 1회 위임, 수신자 그대로 전달
    composer.compose_and_send.assert_awaited_once()
    to_email, instruction = composer.compose_and_send.await_args.args
    assert to_email == "a@b.com"
    # 온톨로지 지시(구조·내용)가 instruction에 주입됨
    assert "회의 일정 변경 문의" in instruction
    assert "인사말" in instruction and "맺음말" in instruction

    assert result.status == "sent"
    assert result.detail == "sent"
