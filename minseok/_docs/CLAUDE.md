# CLAUDE.md — 백엔드 (minseok)

공통 원칙 → [[CLAUDE|CLAUDE (루트)]] · 엔티티 규칙 → [[entitiy-rules]] · 스캐폴드 → [[scaffold-rules]]

---

## 프로젝트 구조

```
minseok/
├── apps/
│   ├── star_craft/     # ★ 허브 — 앱 간 컨텍스트 라우팅·온톨로지 상위 개념 (아래 "스타 토폴로지" 참고)
│   ├── titanic/        # ML 파이프라인 (CSV 업로드, 생존 예측, Kiwi NLP, Ollama 채팅)
│   ├── sherlock_homes/ # 12 캐릭터 헥사고날 실습 앱
│   ├── lion_king/      # 12 캐릭터 헥사고날 실습 앱
│   ├── silicon_valley/
│   ├── kingsman/
│   ├── avengers/
│   └── jobs/
├── core/
│   ├── config.py                          # DATABASE_URL 등 환경변수
│   └── matrix/
│       ├── grid_neo_theone_base.py        # SQLAlchemy DeclarativeBase
│       └── grid_oracle_database_manager.py  # 엔진·세션·create_all_tables
├── main.py             # FastAPI 앱 진입점 (lifespan: init_engine → create_all_tables → dispose_engine)
├── requirements.txt
└── Dockerfile
```

새 앱 추가 시 `apps/` 하위에 동일한 헥사고날 구조를 따른다.

---

## 아키텍처 — 헥사고날 / 클린 / DDD + SOLID

```
<app>/
├── domain/
│   └── entities/           # 순수 도메인 엔티티·값객체 — 외부 의존 금지
├── app/
│   ├── ports/
│   │   ├── input/          # UseCase 인터페이스 (ABC + @abstractmethod)
│   │   └── output/         # Repository 인터페이스 (ABC + @abstractmethod)
│   ├── use_cases/          # Interactor 구현체 (ports/input 구현)
│   └── dtos/               # 레이어 간 전달 객체 (@dataclass / Pydantic BaseModel)
├── adapter/
│   ├── inbound/
│   │   └── api/
│   │       ├── __init__.py      # PEP 562 lazy loading (아래 참고)
│   │       ├── schemas/         # Pydantic 입력 스키마
│   │       └── v1/              # APIRouter 파일들
│   └── outbound/
│       ├── orm/            # SQLAlchemy Mapped 모델
│       ├── pg/             # PgRepository 구현체
│       └── mappers/        # ORM ↔ DTO 변환
├── dependencies/           # FastAPI Depends 공급자 (2-function 패턴)
└── tests/
    ├── conftest.py         # sys.path 설정
    ├── app/use_cases/      # 유스케이스 단위 테스트
    └── test_korean_ai.py   # @pytest.mark.ollama 통합 테스트
```

**의존 방향**: `adapter → app → domain` (역방향 절대 금지)

---

## 스타 토폴로지 — 앱 간 구조 (허브-스포크)

헥사고날(`adapter → app → domain`)이 **앱 내부** 의존을 고정한다면, 스타 토폴로지는 **앱 사이** 의존을 고정한다. 두 규칙은 층위가 다르며 함께 강제된다. (카파시式 하네스: 비선형 연결이 메시로 무너지지 않도록 경계를 배선처럼 묶는다.)

- **허브(Hub) = `apps/star_craft`** — 온톨로지 상위 개념, 앱 간 컨텍스트 라우팅, 전역 인덱스/공유 상태의 단일 교차점.
- **스포크(Spoke) = `star_craft`를 제외한 `apps/` 하위 전부** (`titanic`, `lion_king`, `sherlock_homes`, `avengers`, `kingsman`, `jobs`, `silicon_valley` …) — 허브에 연결되는 독립 도메인 노드. 새 앱은 기본적으로 스포크다.

### 의존 규칙

| 방향 | 허용 | 이유 |
|------|------|------|
| 스포크 → 허브 | ✅ 허용 | 스포크는 허브가 공개한 포트/인터페이스에만 의존한다 |
| 스포크 → 스포크 | ⛔ 금지 | 직접 임포트·순환 참조 절대 금지. 교차 도메인 협력은 반드시 허브 경유 |
| 허브 → 스포크 | ⛔ 금지 | 허브가 특정 스포크를 알면 허브가 비대해지고 스타가 메시로 무너진다 |

- 스포크 A가 스포크 B의 기능이 필요하면, B를 직접 임포트하지 않는다. 허브에 그 협력을 표현하는 포트를 두고 **허브를 통해** 호출한다.
- 허브는 스포크의 **추상(포트/DTO)** 에만 의존할 수 있고, 스포크의 구체 구현(`adapter`/`use_cases`)에는 의존하지 않는다 — 의존 역전을 유지한다.

### `core/`와의 구분

앱 간 공유 채널은 두 개이며 섞지 않는다.

- `core/` — 순수 **인프라** 공유(DB 세션·`Base`·config). 도메인 개념 없음. (기존 [임포트 규칙](#임포트-규칙)대로 `core/` 경유.)
- `star_craft`(허브) — **도메인·온톨로지** 차원의 앱 간 협력·라우팅.

> 이 토폴로지 규칙(스포크↔스포크 직접 임포트 금지, 순환 참조 금지)과 클린 아키텍처 계층은 사람 리뷰가 아니라 정적 분석으로 강제한다. 코드 의존성은 [`.importlinter`](../.importlinter)(import-linter), 문서/온톨로지 링크는 `scripts/validate_harness.py`가 검사한다. 사용법 → [[harness]].

---

## DI 공급자 — 2-function 패턴

모든 앱의 `dependencies/` 파일은 반드시 2-function 패턴을 사용한다.

```python
# dependencies/crew_smith_captain_provider.py
def get_smith_captain_repository(
        db: AsyncSession = Depends(get_db)
) -> SmithCaptainRepository:
    return SmithCaptainPgRepository(session=db)

def get_smith_captain_use_case(
        repository: SmithCaptainRepository = Depends(get_smith_captain_repository)
) -> SmithCaptainUseCase:
    return SmithCaptainInteractor(repository=repository)
```

- 함수명 규칙: `get_{char_keyword}_repository` + `get_{char_keyword}_use_case`
- `char_keyword` = 파일 접두사에서 그룹 접두사 제거 (예: `pride_simba_king` → `simba_king`)
- 단, `passenger_jack_trainer` → `get_jack_train_use_case` (r 생략, 강사 코드 기준)
- Router에서는 항상 `Depends(get_xxx_use_case)` 만 참조한다.

---

## api/__init__.py — PEP 562 Lazy Loading 패턴

각 앱의 `adapter/inbound/api/__init__.py`는 반드시 아래 패턴으로 작성한다.  
이유: schemas 서브모듈 임포트 시 라우터 체인이 즉시 로드되지 않도록 지연한다.

```python
from __future__ import annotations

_titanic_router = None

def __getattr__(name: str):
    global _titanic_router
    if name == "titanic_router":
        if _titanic_router is None:
            _titanic_router = _build_titanic_router()
        return _titanic_router
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

def _build_titanic_router():
    from fastapi import APIRouter
    from titanic.adapter.inbound.api.v1.crew_smith_captain_router import smith_captain_router
    # ... 나머지 라우터 임포트
    router = APIRouter(prefix="/titanic", tags=["titanic"])
    router.include_router(smith_captain_router)
    return router
```

---

## 임포트 규칙

- 컨테이너 `WORKDIR`은 `/app` (= `minseok/` 직접 마운트).
- **`minseok.apps.xxx` 절대 경로 임포트 금지.**
- 같은 앱 내부: `from titanic.app.ports.input.xxx import Xxx`
- 앱 간 공유가 필요하면 `core/` 모듈을 통해 임포트한다.
- `main.py`는 `sys.path.insert(0, apps_dir)` 로 apps 경로를 등록한다.

---

## DB / ORM 규칙

엔티티 정의 시 [[entitiy-rules]] 규칙을 자동 적용한다.

핵심 요약:
- **SQLAlchemy 2.0 스타일** (`Mapped[...]` + `mapped_column(...)`) 만 사용.
- 모든 테이블은 `id: Mapped[int] = mapped_column(primary_key=True)` 를 가진다.
- 비즈니스 식별자는 `unique=True` 별도 컬럼으로 분리한다.

세션 패턴:
```python
from core.matrix.grid_oracle_database_manager import get_db  # AsyncSession 제너레이터
from core.matrix.grid_neo_theone_base import Base             # DeclarativeBase
```

---

## 테스트 규칙

- `pytest + pytest-asyncio` 사용. `@pytest.mark.asyncio` 는 `pytest.ini` 에서 `asyncio_mode = auto` 로 자동 적용.
- 유스케이스 테스트는 `MagicMock + AsyncMock` 으로 Repository를 목킹한다. 실제 DB 불필요.
- Ollama 연동 테스트는 `@pytest.mark.ollama` 마크 사용, 기본 실행에서 제외.
- `conftest.py` 에서 `sys.path` 로 `apps/` 와 `minseok/` 경로를 등록한다.

---

## 앱별 CLAUDE.md

새 앱 추가 시 `apps/<앱명>/_docs/CLAUDE.md` 를 생성하고  
도메인 용어, 역할, 캐릭터 구성, 특이사항을 기록한다.

---

## 머신러닝 데이터 분석 원칙

### Categorical — 카테고리로 묶이는 데이터

**nominal** : 이름 기반 척도
순서 없이 구분만 가능한 데이터
예) 청팀, 홍팀, 백팀

**ordinal** : 순서 기반 척도
자료 사이에 서열이 있는 데이터
예) 이길 가능성 1.매우낮음 2.낮음 3.보통 4.높음 5.매우높음

### Quantitative — 숫자로 셀 수 있는 데이터

**interval** : 간격 기반 척도
기준점(절대 0) 없이 일정 구간을 갖는 데이터 — 배율 비교 불가
예) 시간대, 온도, pH ("10배 덥다" 불가능)

**ratio** : 비율 기반 척도
절대 0이 존재하여 배율 비교가 가능한 데이터
예) 나이, 금액, 몸무게 ("10배 많다" 가능)

---

## async def vs def 결정 규칙

메소드를 작성할 때 `async`를 붙일지 여부는 **작업 성격**으로 결정한다.

| 작업 성격 | 예시 | 형태 |
|-----------|------|------|
| I/O-bound | DB 조회, LLM 호출, HTTP 요청, 파일 읽기 | `async def` |
| CPU-bound | Kiwi 형태소 분석, 수치 계산, 자료구조 변환 | `def` |

**잘못된 패턴** — `async def`를 붙여도 Kiwi가 CPU를 점유하는 시간은 그대로 이벤트 루프를 막는다. `async` 표시만 붙어 비블로킹인 것처럼 보이지만 실제로는 블로킹이라 더 혼란스럽다.

**올바른 패턴** — CPU 작업이 무거워 이벤트 루프 블로킹이 실제 문제가 될 때는 메소드를 `async`로 바꾸지 말고, **호출 측에서 스레드풀로 분리**한다.

```python
# 호출 측 (async 컨텍스트 안)
import asyncio
result = await asyncio.to_thread(use_case.analyze_intent, question)
```

포트(ABC)와 인터렉터 모두 `def` / `async def`를 일치시킨다. 추상 메소드가 `def`이면 구현체도 `def`로 작성해야 호출 측이 `await` 없이 직접 호출할 수 있다.
