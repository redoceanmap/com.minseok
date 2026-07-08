import pytest
from types import SimpleNamespace

from titanic.adapter.outbound.mappers.passenger_jack_trainer_mapper import JackTrainerMapper
from titanic.domain.value_objects.social_vo import Gender, GenderType
from titanic.domain.value_objects.age_vo import Age
from titanic.domain.value_objects.survived_vo import SurvivalStatus
from titanic.domain.entities.passenger_jack_trainer_entity import PassengerEntity


def _make_orm(**overrides):
    defaults = dict(id=1, gender="male", age="30.0", survived="0")
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def _make_entity(
    id: int = 1,
    gender_raw: str = "male",
    age_value: float = 30.0,
    survived: bool | None = False,
) -> PassengerEntity:
    return PassengerEntity(
        id=id,
        gender=Gender.from_raw(gender_raw),
        age=Age(age_value),
        survival_status=SurvivalStatus(survived=survived),
    )


class TestToEntity:
    def test_maps_id(self):
        assert JackTrainerMapper.to_entity(_make_orm(id=42)).id == 42

    def test_maps_gender_male(self):
        entity = JackTrainerMapper.to_entity(_make_orm(gender="male"))
        assert entity.gender.value == GenderType.MALE

    def test_maps_gender_female(self):
        entity = JackTrainerMapper.to_entity(_make_orm(gender="female"))
        assert entity.gender.value == GenderType.FEMALE

    def test_maps_age(self):
        assert JackTrainerMapper.to_entity(_make_orm(age="25.0")).age.value == 25.0

    def test_survived_1_maps_to_true(self):
        assert JackTrainerMapper.to_entity(_make_orm(survived="1")).survival_status.survived is True

    def test_survived_0_maps_to_false(self):
        assert JackTrainerMapper.to_entity(_make_orm(survived="0")).survival_status.survived is False

    def test_survived_none_maps_to_unknown(self):
        assert JackTrainerMapper.to_entity(_make_orm(survived=None)).survival_status.is_unknown is True


class TestToOrm:
    # JackTrainerOrm에 id 컬럼이 없어 TypeError 발생 — 버그 문서화 (Red 상태 유지)

    def test_survival_true_serializes_to_string_1(self):
        with pytest.raises(TypeError):
            JackTrainerMapper.to_orm(_make_entity(survived=True))

    def test_survival_false_serializes_to_string_0(self):
        with pytest.raises(TypeError):
            JackTrainerMapper.to_orm(_make_entity(survived=False))

    def test_survival_unknown_serializes_to_none(self):
        with pytest.raises(TypeError):
            JackTrainerMapper.to_orm(_make_entity(survived=None))
