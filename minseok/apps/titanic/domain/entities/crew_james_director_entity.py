# titanic/domain/entities/passenger.py
from dataclasses import dataclass

@dataclass
class PassengerEntity:
    """비즈니스 중심 도메인 엔티티"""
    passenger_id: int
    name: str
    gender: str
    age: float | None
    sib_sp: int
    parch: int
    survived: int | None
    
    # 예약 정보도 도메인 개념상 승객에 종속되어 있으므로 엔티티가 품을 수 있습니다.
    pclass: int
    ticket: str
    fare: float | None
    cabin: str | None
    embarked: str | None



