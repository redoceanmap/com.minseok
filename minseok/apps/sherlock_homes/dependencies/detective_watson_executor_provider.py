from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from sherlock_homes.adapter.outbound.gateways.detective_watson_executor_n8n_gateway import WatsonExecutorN8nGateway
from sherlock_homes.adapter.outbound.repositories.contact_directory_repository import ContactDirectoryRepository
from sherlock_homes.app.ports.input.detective_watson_executor_use_case import WatsonExecutorUseCase
from sherlock_homes.app.ports.output.detective_watson_executor_directory_port import ContactDirectoryPort
from sherlock_homes.app.ports.output.detective_watson_executor_port import WatsonExecutorPort
from sherlock_homes.app.use_cases.detective_watson_executor_interactor import WatsonExecutorInteractor


def get_watson_executor_repository() -> WatsonExecutorPort:
    return WatsonExecutorN8nGateway()


def get_contact_directory(db: AsyncSession = Depends(get_db)) -> ContactDirectoryPort:
    return ContactDirectoryRepository(session=db)


def get_watson_executor_use_case(
    repository: WatsonExecutorPort = Depends(get_watson_executor_repository),
    directory: ContactDirectoryPort = Depends(get_contact_directory),
) -> WatsonExecutorUseCase:
    return WatsonExecutorInteractor(port=repository, directory=directory)
