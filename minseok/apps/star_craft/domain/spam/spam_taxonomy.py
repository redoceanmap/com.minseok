from __future__ import annotations

from star_craft.domain.spam.spam_category import SpamCategory

# 스팸 분류 온톨로지: 카테고리 ↔ 지시 키워드(개념의 속성).
# 판정 규칙(spam_rules)이 이 트리를 참조한다. LEGITIMATE은 어떤 카테고리에도
# 걸리지 않을 때의 기본값이므로 키워드를 두지 않는다.
SPAM_TAXONOMY: dict[SpamCategory, tuple[str, ...]] = {
    SpamCategory.PHISHING: ("verify your account", "계정 확인", "login", "비밀번호 재설정"),
    SpamCategory.ADVERTISING: ("sale", "할인", "광고", "쿠폰", "구독"),
    SpamCategory.MALWARE: (".exe", "invoice.zip", "첨부파일 실행", "attachment"),
    SpamCategory.SCAM: ("당첨", "lottery", "송금", "상속", "investment"),
}
