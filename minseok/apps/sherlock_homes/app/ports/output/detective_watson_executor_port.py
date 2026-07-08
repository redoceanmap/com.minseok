from __future__ import annotations

from abc import ABC, abstractmethod


class WatsonExecutorPort(ABC):

    @abstractmethod
    async def send(self, to_email: str, subject: str, body: str, name: str = "") -> dict:
        '''완성된 제목·본문을 외부 발송 채널(n8n/Gmail)로 전달한다. name=받는 사람 이름(주소록).'''
        ...
