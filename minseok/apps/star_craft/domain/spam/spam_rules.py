from __future__ import annotations

from star_craft.domain.spam.spam_category import SpamCategory
from star_craft.domain.spam.spam_taxonomy import SPAM_TAXONOMY


def classify_by_keywords(text: str) -> SpamCategory:
    '''텍스트를 온톨로지 키워드와 대조해 카테고리를 판정한다.

    I/O 없는 순수 함수. 먼저 매칭되는 카테고리를 반환하고, 아무것도 걸리지 않으면
    LEGITIMATE을 반환한다.
    '''
    lowered = text.lower()
    for category, keywords in SPAM_TAXONOMY.items():
        if any(keyword.lower() in lowered for keyword in keywords):
            return category
    return SpamCategory.LEGITIMATE
