import pytest
from types import SimpleNamespace

from titanic.domain.entities.passenger_jack_trainer_entity import PassengerEntity
from titanic.domain.value_objects.social_vo import Gender
from titanic.domain.value_objects.age_vo import Age
from titanic.domain.value_objects.survived_vo import SurvivalStatus


def _make_entity(
    id: int = 1,
    gender_raw: str | None = "male",
    age_value: float | None = 30.0,
    survived: bool | None = None,
) -> PassengerEntity:
    return PassengerEntity(
        id=id,
        gender=Gender.from_raw(gender_raw),
        age=Age(age_value),
        survival_status=SurvivalStatus(survived=survived),
    )


class TestIsHighRisk:
    def test_male_adult_is_high_risk(self):
        assert _make_entity(gender_raw="male", age_value=30.0).is_high_risk() is True

    def test_female_adult_is_not_high_risk(self):
        assert _make_entity(gender_raw="female", age_value=30.0).is_high_risk() is False

    def test_male_minor_is_not_high_risk(self):
        assert _make_entity(gender_raw="male", age_value=15.0).is_high_risk() is False

    def test_unknown_gender_adult_is_high_risk(self):
        assert _make_entity(gender_raw=None, age_value=30.0).is_high_risk() is True


class TestRecordSurvival:
    def test_record_true_updates_survival_status(self):
        entity = _make_entity(survived=None)
        entity.record_survival(True)
        assert entity.survival_status.survived is True

    def test_record_false_updates_survival_status(self):
        entity = _make_entity(survived=True)
        entity.record_survival(False)
        assert entity.survival_status.survived is False


class TestEquality:
    def test_same_id_entities_are_equal(self):
        assert _make_entity(id=1) == _make_entity(id=1)

    def test_different_id_entities_are_not_equal(self):
        assert _make_entity(id=1) != _make_entity(id=2)

    def test_same_id_entities_have_same_hash(self):
        assert hash(_make_entity(id=1)) == hash(_make_entity(id=1))

    def test_entities_deduplicated_in_set_by_id(self):
        result = {_make_entity(id=1), _make_entity(id=1), _make_entity(id=2)}
        assert len(result) == 2


class TestFromOrm:
    def test_maps_all_fields_correctly(self):
        orm = SimpleNamespace(
            id=5,
            gender="female",
            age="42.0",
            survived="1",
        )
        entity = PassengerEntity.from_orm(orm)

        assert entity.id == 5
        assert entity.gender.is_female() is True
        assert entity.age.value == 42.0
        assert entity.survival_status.survived is True

    def test_none_optional_fields_map_correctly(self):
        orm = SimpleNamespace(id=1, gender=None, age=None, survived=None)
        entity = PassengerEntity.from_orm(orm)

        assert entity.survival_status.is_unknown is True
