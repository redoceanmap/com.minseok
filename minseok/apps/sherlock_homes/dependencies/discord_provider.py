from fastapi import Depends

from sherlock_homes.adapter.outbound.repositories.discord_repository import DiscordRepository
from sherlock_homes.app.ports.input.discord_use_case import DiscordUseCase
from sherlock_homes.app.ports.output.discord_port import DiscordPort
from sherlock_homes.app.use_cases.discord_interactor import DiscordInteractor


def get_discord_repository() -> DiscordPort:
    return DiscordRepository()


def get_discord_use_case(
    repository: DiscordPort = Depends(get_discord_repository),
) -> DiscordUseCase:
    return DiscordInteractor(repository=repository)
