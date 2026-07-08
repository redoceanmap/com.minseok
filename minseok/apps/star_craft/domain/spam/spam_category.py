from __future__ import annotations

from enum import Enum


class SpamCategory(str, Enum):
    '''스팸 분류 온톨로지의 최상위 개념(카테고리).

    허브(star_craft)가 공개하는 전역 온톨로지의 일부이며, 외부 의존 없는 순수 도메인이다.
    LEGITIMATE은 어떤 스팸 카테고리에도 해당하지 않을 때의 기본값이다.
    '''

    PHISHING = "phishing"
    ADVERTISING = "advertising"
    MALWARE = "malware"
    SCAM = "scam"
    LEGITIMATE = "legitimate"
