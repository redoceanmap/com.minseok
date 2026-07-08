from __future__ import annotations

from abc import ABC, abstractmethod


class ContactDirectoryPort(ABC):

    @abstractmethod
    async def find_name_by_email(self, email: str) -> str:
        '''이메일로 주소록에서 받는 사람 이름을 찾는다. 없으면 빈 문자열.'''
        ...
