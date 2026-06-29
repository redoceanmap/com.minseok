# 하네스(Harness) — 구조 무결성 검증 도구

> 카파시式 하네스 엔지니어링: 모델·코드·지식 구조가 올바르게 유지되도록, 평가·정적 분석·제약을 배선(harness)처럼 엮어 자동으로 '테스트'한다. 사람 리뷰가 놓치는 구조 위반을 실패로 만든다.

이 저장소는 두 개의 직교하는 구조를 가진다.

- **코드** — 모듈러 모놀리식 + 스타 토폴로지: `star_craft`(허브) 중심, 나머지 앱은 스포크. 앱 내부는 클린 아키텍처(`adapter → app → domain`).
- **문서** — Obsidian WikiLink로 엮인 온톨로지(지식 그래프).

각 구조를 지키는 도구는 아래와 같다. 역할이 겹치지 않게 분리돼 있다.

| 도구 | 검사 대상 | 위치 |
|------|-----------|------|
| **import-linter** | 코드 import 그래프 — 스타 토폴로지 + 클린 아키텍처 | `minseok/.importlinter` |
| **validate_harness.py** | 문서 구조 — 심볼릭/WikiLink 무결성, 고립 노드, 온톨로지 토폴로지 | `scripts/validate_harness.py` |
| **markdownlint-cli2** | MD 표기 스타일 (Obsidian 친화) | `.markdownlint-cli2.jsonc` |

---

## 1. import-linter — 코드 아키텍처 하네스

세 계약을 강제한다.

1. **클린 아키텍처** — 모든 앱에서 `adapter > app > domain` (역방향 import 금지)
2. **스포크 독립** — 스포크끼리 직접 import 금지 (교차 협력은 허브 경유)
3. **허브 격리** — `star_craft`(허브)는 스포크를 import 하지 않음

```bash
pip install -r minseok/requirements.txt            # import-linter 포함
cd minseok && PYTHONPATH=apps lint-imports --config .importlinter
```

`PYTHONPATH=apps`는 `main.py`의 `sys.path.insert(0, "apps")`와 같은 맥락 — 앱을 최상위 패키지(`titanic`, `lion_king` …)로 인식시키기 위함.

## 2. validate_harness.py — 온톨로지/문서 하네스

표준 라이브러리만으로 동작(설치 불필요). 직전 vault 삭제 사고로 생긴 끊긴 심볼릭/WikiLink를 잡아내는 바로 그 검사.

```bash
python3 scripts/validate_harness.py            # 위반 시 종료코드 1
python3 scripts/validate_harness.py --strict   # 고립 노드(경고)도 실패 처리
```

검사: ① 깨진 심볼릭 링크 ② 깨진 WikiLink ③ 고립 노드 ④ 프론트매터 토폴로지(`type: hub|spoke` 선언 노드 한정 — 스포크↔스포크 직접 링크·순환 참조 금지).

> 온톨로지 토폴로지(④)는 `type`/`links` 프론트매터가 있는 노드에만 적용된다. 선언이 없는 기존 문서는 건너뛰므로 점진 도입이 가능하다.

## 3. markdownlint-cli2 — MD 스타일

```bash
npx markdownlint-cli2          # www/ 의 Node 사용
npx markdownlint-cli2 --fix
```

WikiLink '깨짐'은 검사하지 못한다 — 그건 `validate_harness.py`의 몫.

---

## CI / pre-commit 연결

세 도구 모두 위반 시 비정상 종료코드를 반환하므로 그대로 훅에 연결할 수 있다.

```bash
python3 scripts/validate_harness.py \
  && (cd minseok && PYTHONPATH=apps lint-imports --config .importlinter)
```

## 현재 알려진 위반

- **클린 아키텍처 BROKEN** — `lion_king.app.use_cases`·`ports.input`이 `lion_king.adapter.inbound.api.schemas`를 import(9곳). use_case가 어댑터 스키마에 직접 의존하는 계층 역전. 수정 방향: 어댑터 스키마 대신 `app/dtos`를 사용.
