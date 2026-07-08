from fastapi import Depends

from star_craft.app.ports.input.email_request_use_case import EmailRequestUseCase
from star_craft.app.ports.output.email_composer_port import EmailComposerPort
from star_craft.app.use_cases.email_request_interactor import EmailRequestInteractor


def get_email_composer() -> EmailComposerPort:
    '''합성 루트(main.py)의 dependency_overrides로 스포크 구현을 주입한다.

    허브는 구체 스포크를 모르므로 여기서는 구현을 모른다. override 없이 호출되면 설정 오류다.
    '''
    raise NotImplementedError(
        "get_email_composer는 main.py의 dependency_overrides로 스포크 구현을 주입해야 합니다."
    )


def get_email_request_use_case(
        composer: EmailComposerPort = Depends(get_email_composer),
) -> EmailRequestUseCase:
    return EmailRequestInteractor(composer=composer)
