from fastapi import Depends

from sherlock_homes.adapter.outbound.repositories.telegram_repository import TelegramRepository
from sherlock_homes.app.ports.input.telegram_use_case import TelegramUseCase
from sherlock_homes.app.ports.output.telegram_port import TelegramPort
from sherlock_homes.app.use_cases.telegram_interactor import TelegramInteractor


def get_telegram_repository() -> TelegramPort:
    return TelegramRepository()


def get_telegram_use_case(
    repository: TelegramPort = Depends(get_telegram_repository),
) -> TelegramUseCase:
    return TelegramInteractor(repository=repository)
