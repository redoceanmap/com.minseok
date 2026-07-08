from __future__ import annotations

import logging
from typing import Any

import pandas as pd

from titanic.adapter.outbound.orm.passenger_rose_model_strategies import build_all_strategies
from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.output.passenger_jack_trainer_port import JackTrainerPort

logger = logging.getLogger(__name__)


class JackTrainerInteractor(JackTrainerUseCase):

    def __init__(self, repository: JackTrainerPort):
        self.repository = repository
        self._trained_strategies: dict = {}

    def train_model(self, X: pd.DataFrame, y: list[int]) -> dict[str, Any]:
        '''로즈가 제안한 모델들을 훈련시키는 메소드'''
        logger.info("[JackTrainerInteractor] 학습 파이프라인 시작")

        X_train: list[list[float]] = X.values.tolist()

        # 8. 로즈의 10개 전략으로 학습
        self._trained_strategies = {}
        trained_names = []
        for key, StrategyClass in build_all_strategies().items():
            strategy = StrategyClass()
            try:
                strategy.fit(X_train, y)
                self._trained_strategies[key] = strategy
                trained_names.append(strategy.name)
                logger.info(f"[JackTrainerInteractor] {strategy.name} 학습 완료")
            except Exception as e:
                logger.warning(f"[JackTrainerInteractor] {key} 학습 실패 | error={e}")

        return {
            "train_samples": len(X_train),
            "trained_models": trained_names,
            "trained_strategies": self._trained_strategies,  # CalTesterInteractor에 전달
        }

    

    async def predict_survival(self, passenger_data: dict[str, Any]) -> dict[str, Any]:
        '''학습 데이터에서 동일 코호트(성별·연령대)의 경험적 생존율로 예측한다.

        입력은 {gender, age}뿐이므로 전체 ML 피처 모델 대신 코호트 생존율을 사용한다.
        코호트가 비면 {}를 반환해 호출 측(스미스)이 도메인 규칙으로 우회하게 한다.
        '''
        gender = passenger_data.get("gender")
        age = passenger_data.get("age")

        def _to_float(v):
            try:
                return float(v)
            except (TypeError, ValueError):
                return None

        rows = await self.repository.get_training_data()
        cohort = [r for r in rows if str(r.get("survived")).strip() in ("0", "1")]

        if gender in ("male", "female"):
            cohort = [r for r in cohort if r.get("gender") == gender]
        if age is not None:
            cohort = [
                r for r in cohort
                if _to_float(r.get("age")) is not None
                and abs(_to_float(r["age"]) - float(age)) <= 8
            ]

        if not cohort:
            return {}

        survived_count = sum(1 for r in cohort if str(r["survived"]).strip() == "1")
        probability = survived_count / len(cohort)
        return {
            "probability": probability,
            "survived": probability >= 0.5,
            "cohort_size": len(cohort),
        }

    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        '''잭 트레이너의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(JackTrainerQuery(
            id=schema.id,
            name=schema.name,
        ))
