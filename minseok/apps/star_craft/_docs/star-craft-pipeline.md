# star_craft 파이프라인 전략 — Graph DB · Vector DB 허브

`apps/star_craft`는 [스타 토폴로지](../../../CLAUDE.md)의 **허브(Hub)** 다. 모든 스포크 앱이 교차하는 단일 지점이며, 온톨로지 상위 개념과 앱 간 컨텍스트 라우팅을 담당한다. 이 문서는 허브가 **도커의 Graph DB·Vector DB에 접속해 GraphRAG 검색을 제공하는 파이프라인**의 설계 전략을 기술한다.

> 상위 원칙 → [[CLAUDE]] · 백엔드 규칙 → [[minseok/_docs/CLAUDE|minseok CLAUDE]] · 허브 도메인 → [[CLAUDE|star_craft CLAUDE]]

---

## 0. 현재 상태 (출발점)

| 항목 | 현황 |
|------|------|
| `docker-compose.yaml` | `backend` / `frontend` / `n8n` 만 존재 — **Graph/Vector DB 없음** |
| `requirements.txt` | `sqlalchemy[asyncio]`, `psycopg` (Postgres만) — graph/vector/임베딩 클라이언트 없음 |
| star_craft 구조 | 헥사고날 스캐폴드만 존재 (`adapter/inbound/mcp/` 폴더 포함, 구현 비어 있음) |
| 합성 LLM | `core/lol/t1_mid_faker_orchestrator.py` 의 EXAONE 3.5 2.4B 오케스트레이터 |

→ 이 전략은 **도커에 두 DB를 신규로 올리고**, 허브가 헥사고날 경계로 접속하는 것을 목표로 한다.

---

## 1. 기술 선택 (결정 — 변경 가능)

| 역할 | 선택 | 근거 | 대안 |
|------|------|------|------|
| **Graph DB** | **Neo4j 5** | 허브의 "온톨로지 상위 개념"과 직결. Cypher로 엔티티·관계 표현, GraphRAG의 사실상 표준. async 드라이버(`neo4j`) 제공 | Memgraph, ArangoDB |
| **Vector DB** | **Qdrant** | 단일 도커 이미지로 가볍게 기동, async 클라이언트(`qdrant-client`), 메타데이터 필터링 강력 | Weaviate, pgvector(기존 Postgres 재사용) |
| **임베딩** | **Ollama 임베딩 모델** (`bge-m3` 등) | 이미 로컬 Ollama 사용 중 — 외부 API/키 불필요, 한국어 강함 | `sentence-transformers` 로컬 |
| **합성(생성)** | **EXAONE 3.5** (`t1_mid_faker_orchestrator`) | 이미 구축된 오케스트레이터 재사용 | — |

> **pgvector 노트:** 별도 Vector DB 없이 기존 Postgres + pgvector로도 가능하다. 다만 본 전략은 요청대로 **Graph·Vector를 독립 서비스로 분리**한다(관심사 분리·확장성). 단순화를 우선한다면 pgvector로 축소할 수 있다.

---

## 2. 아키텍처 개요

```
                    ┌─────────────────────────────────────────┐
   스포크 앱들       │              HUB: star_craft              │
 (titanic, lol …)   │                                           │
        │           │   app/ports/input   (UseCase ABC)         │
        └──────────▶│   app/use_cases     (Interactor)          │
   허브 포트만 의존   │   app/ports/output  (Repository ABC)      │
                    │        │                  │               │
                    │  adapter/outbound/   adapter/outbound/    │
                    │     graph(Neo4j)        vector(Qdrant)    │
                    └────────┼──────────────────┼───────────────┘
                             │                  │
                      ┌──────▼──────┐    ┌──────▼──────┐
                      │  Neo4j      │    │  Qdrant     │   ← docker-compose
                      │  :7687/7474 │    │  :6333      │
                      └─────────────┘    └─────────────┘
                             │
                      ┌──────▼──────┐
                      │ Ollama      │  임베딩 + EXAONE 합성
                      │ :11434      │
                      └─────────────┘
```

- **의존 방향:** `adapter → app → domain` (역방향 금지). 외부 DB 접속은 전부 **outbound 어댑터**에 격리한다.
- **스타 토폴로지 준수:** 스포크는 star_craft의 **포트(`app/ports/input`)** 에만 의존하고, Neo4j/Qdrant 구체 구현은 알지 못한다. 허브가 두 DB를 가진 단일 교차점이다.

---

## 3. 데이터 흐름 파이프라인

### 3-1. 적재(Ingestion) — 쓰기 경로

```
원천 문서/엔티티
   │
   ▼ [1] 정규화      도메인 엔티티 + 청크 분할
   │
   ├─▶ [2a] 임베딩    Ollama(bge-m3) → 벡터 → Qdrant upsert (payload: 출처·엔티티ID)
   │
   └─▶ [2b] 그래프화   엔티티/관계 추출 → Neo4j MERGE (노드·엣지)
   │
   ▼ [3] 정합성 키    Qdrant payload.entity_id ↔ Neo4j 노드 id 로 양쪽을 연결
```

- 두 저장소는 **공통 식별자(`entity_id`)** 로 묶는다. 벡터 검색 결과 → 그래프 노드로 점프할 수 있어야 한다.
- 적재는 멱등(`MERGE`/`upsert`)으로 재실행 안전하게.

### 3-2. 검색(Retrieval) — 읽기 경로 (GraphRAG)

```
질의(query)
   │
   ▼ [1] 질의 임베딩            Ollama → query vector
   │
   ▼ [2] 벡터 검색             Qdrant top-k 유사 청크 → seed entity_id 집합
   │
   ▼ [3] 그래프 확장           Neo4j: seed에서 N-hop 이웃·관계 탐색 (Cypher)
   │
   ▼ [4] 컨텍스트 결합          벡터 청크 + 그래프 서브그래프 → 프롬프트 컨텍스트
   │
   ▼ [5] 합성                  EXAONE(t1_mid_faker_orchestrator) → 최종 답변
```

→ 벡터(의미 유사) + 그래프(구조·관계)를 합쳐 단일 벡터 RAG보다 **다단계 추론·출처 추적**에 강하다.

---

## 4. 헥사고날 매핑 (구현 배치)

> 명명은 star_craft 테마(StarCraft) 기준으로 잡되, 확정 전 [[CLAUDE|star_craft CLAUDE]]에 캐릭터/유닛 체계를 먼저 정의한다. 아래는 배치 위치 제안이다.

```
apps/star_craft/
├── domain/
│   └── entities/                 # 온톨로지 노드·관계 도메인 모델 (순수)
├── app/
│   ├── ports/
│   │   ├── input/                # RetrieveUseCase, IngestUseCase (ABC)
│   │   └── output/
│   │       ├── graph_repository.py   # GraphRepository ABC (upsert_node, neighbors …)
│   │       └── vector_repository.py  # VectorRepository ABC (upsert, search …)
│   ├── use_cases/                # GraphRagInteractor (검색·적재 오케스트레이션)
│   └── dtos/                     # RetrievalQuery / RetrievalResult
├── adapter/
│   ├── inbound/
│   │   ├── api/v1/               # FastAPI 라우터 (스포크·외부 진입점)
│   │   └── mcp/                  # MCP 서버 진입점 (기존 폴더)
│   └── outbound/
│       ├── graph/                # Neo4jGraphRepository (neo4j async driver)
│       ├── vector/               # QdrantVectorRepository (qdrant-client)
│       └── embedding/            # OllamaEmbedder (Ollama embeddings 호출)
└── dependencies/                 # 2-function DI 공급자
```

### 포트 인터페이스 골격 (예시)

```python
# app/ports/output/vector_repository.py
from abc import ABC, abstractmethod

class VectorRepository(ABC):
    @abstractmethod
    async def upsert(self, entity_id: str, vector: list[float], payload: dict) -> None: ...

    @abstractmethod
    async def search(self, query_vector: list[float], top_k: int) -> list[dict]: ...
```

```python
# app/ports/output/graph_repository.py
from abc import ABC, abstractmethod

class GraphRepository(ABC):
    @abstractmethod
    async def upsert_node(self, entity_id: str, labels: list[str], props: dict) -> None: ...

    @abstractmethod
    async def neighbors(self, entity_id: str, hops: int) -> list[dict]: ...
```

- I/O-bound(DB·임베딩·LLM)이므로 포트·구현 모두 `async def` ([[minseok/_docs/CLAUDE|async 규칙]]).
- DI는 `dependencies/`에서 2-function 패턴(`get_..._repository` → `get_..._use_case`).

---

## 5. 도커 구성 추가안

`docker-compose.yaml`에 두 서비스를 추가한다(예시 — 포트·인증은 환경에 맞게).

```yaml
  neo4j:
    image: neo4j:5
    ports:
      - "7474:7474"   # HTTP 브라우저
      - "7687:7687"   # Bolt 드라이버
    environment:
      - NEO4J_AUTH=neo4j/please_change
    volumes:
      - neo4j_data:/data

  qdrant:
    image: qdrant/qdrant
    ports:
      - "6333:6333"   # REST/gRPC
    volumes:
      - qdrant_data:/qdrant/storage

volumes:
  neo4j_data:
  qdrant_data:
```

> Ollama는 호스트(macOS)에서 구동 중이므로 컨테이너 backend에서 접근하려면 `host.docker.internal:11434`를 사용한다. 로컬(비도커) 실행이면 `localhost:11434`.

---

## 6. 의존성 추가

`minseok/requirements.txt`:

```
neo4j==5.*          # async Bolt 드라이버
qdrant-client       # async 지원
# 임베딩은 기존 ollama 패키지의 embeddings API 사용 (추가 설치 불필요)
```

---

## 7. 환경변수 (`core/config.py` 확장)

```python
NEO4J_URI      = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER     = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
QDRANT_URL     = os.getenv("QDRANT_URL", "http://localhost:6333")
OLLAMA_HOST    = os.getenv("OLLAMA_HOST", "http://localhost:11434")
EMBED_MODEL    = os.getenv("EMBED_MODEL", "bge-m3")
```

> 비밀번호는 코드/문서에 하드코딩하지 않는다. `.env`로 주입한다.

---

## 8. 스타 토폴로지 경계 (강제 규칙)

- 스포크는 **`star_craft`의 입력 포트**만 임포트한다. Neo4j/Qdrant 클라이언트나 outbound 어댑터를 스포크가 직접 임포트하면 위반.
- 허브는 스포크의 **구체 구현에 의존하지 않는다** — 두 DB는 허브 내부 인프라로 캡슐화한다.
- 이 경계는 [`.importlinter`](../../../.importlinter)로 정적 강제한다(스포크↔스포크 금지, 순환 금지).

---

## 9. 단계별 로드맵 (단계 → 검증)

```text
1. docker-compose에 neo4j·qdrant 추가
   → 검증: `docker compose up` 후 7474(브라우저)·6333(REST) 응답 확인
2. requirements 추가 + core/config 환경변수
   → 검증: 파이썬에서 두 드라이버 import·핑(서버 연결) 성공
3. output 포트 ABC 2종 정의 (graph / vector)
   → 검증: ABC 인스턴스화 시 TypeError(추상 메서드 미구현) 확인
4. outbound 어댑터 구현 (Neo4j / Qdrant / Ollama 임베더)
   → 검증: upsert→search 왕복 통합 테스트(@pytest.mark.ollama 류 마크)
5. GraphRagInteractor + DI 공급자
   → 검증: mock 레포로 유스케이스 단위 테스트(검색 흐름 4→5 단계 호출 순서)
6. inbound(api/v1 또는 mcp) 진입점 연결
   → 검증: 질의 1건 end-to-end — 벡터검색→그래프확장→EXAONE 합성 응답
```

---

## 10. 열린 결정 (확정 필요)

1. **Vector DB:** Qdrant vs pgvector(기존 Postgres 재사용으로 단순화) — 분리 유지 여부.
2. **임베딩 모델:** `bge-m3`(다국어) vs 한국어 특화 모델 — Ollama로 받을 모델 확정.
3. **적재 트리거:** 수동 배치 vs n8n(이미 도커에 존재) 워크플로 연동.
4. **inbound 우선순위:** FastAPI API 먼저 vs MCP 서버 먼저.
5. **명명 체계:** star_craft 캐릭터/유닛 기반 식별자 — [[CLAUDE|star_craft CLAUDE]]에 선정의.
