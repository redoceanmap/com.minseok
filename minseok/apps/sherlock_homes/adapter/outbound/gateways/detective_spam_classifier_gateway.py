from __future__ import annotations

from core.lol.t1_mid_faker_orchestrator import EXAONE_2_4B, orchestrator
from sherlock_homes.app.ports.output.detective_spam_classifier_port import SpamClassifierPort


class ExaoneSpamClassifierGateway(SpamClassifierPort):
    '''오케스트레이터(Faker)에 EXAONE 2.4B를 넘겨 스팸 분류 출력 포트를 구현한 게이트웨이.'''

    async def classify(self, prompt: str) -> str:
        return await orchestrator.orchestrate(prompt, model=EXAONE_2_4B)
