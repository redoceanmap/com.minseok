from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class JackTrainerUseCase(ABC):

    @abstractmethod
    def train_model(self, X, y) -> dict[str, Any]:
        '''로즈가 제안한 모델들을 훈련시키는 메소드'''

    @abstractmethod
    async def predict_survival(self, passenger_data: dict[str, Any]) -> dict[str, Any]:
        ...
