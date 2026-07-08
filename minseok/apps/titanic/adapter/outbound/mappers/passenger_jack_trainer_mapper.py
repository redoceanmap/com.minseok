from __future__ import annotations

from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import JackTrainerOrm
from titanic.domain.entities.passenger_jack_trainer_entity import PassengerEntity
from titanic.domain.value_objects.social_vo import Gender
from titanic.domain.value_objects.age_vo import Age
from titanic.domain.value_objects.survived_vo import SurvivalStatus


class JackTrainerMapper:

    @staticmethod
    def to_entity(orm: JackTrainerOrm) -> PassengerEntity:
        return PassengerEntity(
            id=orm.id,
            gender=Gender.from_raw(orm.gender),
            age=Age.from_raw(orm.age),
            survival_status=SurvivalStatus.from_raw(orm.survived),
        )

    @staticmethod
    def to_orm(entity: PassengerEntity) -> JackTrainerOrm:
        if entity.survival_status.survived is True:
            survival_raw = "1"
        elif entity.survival_status.survived is False:
            survival_raw = "0"
        else:
            survival_raw = None

        return JackTrainerOrm(
            id=entity.id,
            gender=str(entity.gender),
            age=str(entity.age.value) if entity.age.value is not None else None,
            survived=survival_raw,
        )
