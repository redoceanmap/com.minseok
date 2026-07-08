from __future__ import annotations

import httpx

from core.config import N8N_WEBHOOK_TOKEN, N8N_WEBHOOK_URL
from sherlock_homes.app.ports.output.detective_watson_executor_port import WatsonExecutorPort


class WatsonExecutorN8nGateway(WatsonExecutorPort):
    '''n8n 웹훅으로 발송 요청을 전달하는 출력 게이트웨이. Gmail 자격증명은 n8n이 보유한다.'''

    async def send(self, to_email: str, subject: str, body: str, name: str = "") -> dict:
        payload = {"to": to_email, "subject": subject, "body": body, "name": name}
        headers = {"X-Webhook-Token": N8N_WEBHOOK_TOKEN}

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(N8N_WEBHOOK_URL, json=payload, headers=headers)
            response.raise_for_status()
            return {"status_code": response.status_code, "response": response.text}
