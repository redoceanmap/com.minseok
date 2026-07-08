from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_homes.app.dtos.detective_watson_executor_dto import DispatchCommand, DispatchResult


class WatsonExecutorUseCase(ABC):

    @abstractmethod
    async def dispatch(self, command: DispatchCommand) -> DispatchResult:
        '''주제로 이메일을 작성해 지정한 주소로 발송한다.'''
        ...
