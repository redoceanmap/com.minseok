from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from sherlock_homes.adapter.outbound.repositories.inbound_mail_repository import InboundMailRepository
from sherlock_homes.app.ports.input.inbound_mail_use_case import InboundMailUseCase
from sherlock_homes.app.ports.output.inbound_mail_port import InboundMailPort
from sherlock_homes.app.use_cases.inbound_mail_interactor import InboundMailInteractor


def get_inbound_mail_repository(db: AsyncSession = Depends(get_db)) -> InboundMailPort:
    return InboundMailRepository(session=db)


def get_inbound_mail_use_case(
    repository: InboundMailPort = Depends(get_inbound_mail_repository),
) -> InboundMailUseCase:
    return InboundMailInteractor(repository=repository)
