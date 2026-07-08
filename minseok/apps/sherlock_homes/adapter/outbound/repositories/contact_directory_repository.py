from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sherlock_homes.adapter.outbound.orm.juso_orm import JusoOrm
from sherlock_homes.app.ports.output.detective_watson_executor_directory_port import ContactDirectoryPort


class ContactDirectoryRepository(ContactDirectoryPort):
    '''주소록(juso_contacts)에서 이메일로 이름을 조회하는 어댑터.'''

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_name_by_email(self, email: str) -> str:
        result = await self.session.execute(
            select(JusoOrm.name).where(JusoOrm.email == email)
        )
        return result.scalar_one_or_none() or ""
