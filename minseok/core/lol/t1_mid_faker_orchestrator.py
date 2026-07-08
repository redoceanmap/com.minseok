"""T1 미드 Faker 오케스트레이터.

LoL T1의 미드 캐리(Faker)가 경기를 지휘하듯, 등록된 LLM 모델을 받아
추론을 지휘하는 중앙 오케스트레이터. EXAONE 3.5 7.8B(Ollama)를
기본 모델로 등록한다.
"""
from __future__ import annotations

from dataclasses import dataclass

from ollama import AsyncClient


@dataclass(frozen=True)
class ModelSpec:
    """오케스트레이터에 등록되는 모델 명세."""

    name: str   # Ollama 모델 태그 (예: "exaone3.5:7.8b")
    label: str  # 사람이 읽는 이름


class T1MidFakerOrchestrator:
    """등록된 모델 중 하나를 골라 채팅 추론을 수행하는 오케스트레이터."""

    def __init__(self, host: str | None = None) -> None:
        self._client = AsyncClient(host=host) if host else AsyncClient()
        self._registry: dict[str, ModelSpec] = {}
        self._default: str | None = None

    def register(self, key: str, spec: ModelSpec, *, default: bool = False) -> None:
        """모델을 레지스트리에 등록한다. 첫 등록 모델은 자동으로 기본값이 된다."""
        self._registry[key] = spec
        if default or self._default is None:
            self._default = key

    async def orchestrate(self, prompt: str, *, model: str | None = None) -> str:
        """프롬프트를 추론한다. model을 넘기면 그 모델로(스포크가 2.4B 전달),
        미지정이면 등록된 기본 모델(Faker 7.8B)로 추론한다."""
        if model is None:
            if self._default is None:
                raise RuntimeError("등록된 모델이 없습니다. register()로 먼저 등록하세요.")
            model = self._registry[self._default].name

        response = await self._client.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"]


# --- 오케스트레이터는 하나. Faker는 7.8B만 보유한다. ---
EXAONE_3_5_7_8B = ModelSpec(name="exaone3.5:7.8b", label="EXAONE 3.5 7.8B")

# 스포크(sherlock_homes 메일작성·스팸분류)가 orchestrate(model=...)로 넘겨 쓰는 모델 태그.
EXAONE_2_4B = "exaone3.5:2.4b"

orchestrator = T1MidFakerOrchestrator()
orchestrator.register("exaone-7.8b", EXAONE_3_5_7_8B, default=True)  # Faker 보유 모델(7.8B 전용)


if __name__ == "__main__":
    import asyncio

    answer = asyncio.run(orchestrator.orchestrate("한국어로 짧게 자기소개 해줘."))
    print(answer)
