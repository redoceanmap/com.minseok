from dataclasses import dataclass
from titanic.domain.value_objects.social_vo import Gender
from titanic.domain.value_objects.age_vo import Age
from titanic.domain.value_objects.survived_vo import SurvivalStatus


@dataclass
class PassengerEntity:
    id: int
    gender: Gender
    age: Age
    survival_status: SurvivalStatus

    @classmethod
    def from_orm(cls, orm) -> "PassengerEntity":
        return cls(
            id=orm.id,
            gender=Gender.from_raw(orm.gender),
            age=Age.from_raw(orm.age),
            survival_status=SurvivalStatus.from_raw(orm.survived),
        )

    def is_high_risk(self) -> bool:
        return not self.gender.is_female() and not self.age.is_minor

    def record_survival(self, survived: bool) -> None:
        object.__setattr__(self, "survival_status", SurvivalStatus(survived=survived))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PassengerEntity):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return (
            f"PassengerEntity("
            f"id={self.id}, gender={self.gender}, "
            f"age={self.age}, survival={self.survival_status})"
        )
