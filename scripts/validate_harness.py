#!/usr/bin/env python3
# =============================================================================
# validate_harness.py — 온톨로지/문서 하네스 (MD 레벨)
# =============================================================================
# 왜 필요한가 (카파시式 하네스):
#   이 저장소의 .md 는 단순 문서가 아니라 Obsidian WikiLink([[..]])로 엮인
#   '지식 그래프(온톨로지)'다. 링크가 깨지거나(예: vault 서브모듈 삭제로 끊긴 링크),
#   고립 노드가 생기거나, 스타 토폴로지(허브-스포크) 규칙을 어기면 지식 구조가
#   조용히 무너진다. 이 스크립트는 그 무결성을 import-linter 처럼 '테스트'한다.
#   실제로 직전의 vault 삭제 사고(끊긴 심볼릭 링크·WikiLink)를 이 검사가 잡아낸다.
#
# 무엇을 검사하나:
#   [1] 깨진 심볼릭 링크        — 타깃이 사라진 링크 (vault 삭제로 발생했던 그 버그)
#   [2] 깨진 WikiLink           — [[대상]] 이 어떤 .md 로도 해석되지 않음
#   [3] 고립 노드(orphan)       — 들어오는/나가는 링크가 하나도 없는 .md (경고)
#   [4] 프론트매터 토폴로지     — type: hub|spoke 선언이 있는 노드에 한해
#                                 스포크↔스포크 직접 링크 금지, 순환 참조 금지 강제
#                                 (선언이 없는 문서는 건너뜀 → 점진 도입 가능)
#
# MD 양식: Obsidian WikiLink ([[note]], [[note|alias]], [[folder/note]],
#          [[note#heading]], 임베드 ![[note]]) 기준.
#
# 실행:   python3 scripts/validate_harness.py
#         python3 scripts/validate_harness.py --strict   # orphan(경고)도 실패 처리
# 종료코드: 위반 있으면 1, 없으면 0 (CI/pre-commit 훅에 그대로 연결 가능)
# 의존성: 표준 라이브러리만 사용 (PyYAML 불필요)
# =============================================================================

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Obsidian vault = 저장소 루트. 아래 디렉토리는 노드가 아니므로 스캔에서 제외.
EXCLUDE_DIRS = {
    ".git", "venv", "node_modules", ".obsidian", "__pycache__", ".pytest_cache",
    # 생성/벤더 디렉토리 (Flutter·iOS·Android) — 온톨로지 노드가 아님
    ".dart_tool", "build", "Pods", ".gradle", "Assets.xcassets",
}

# [[target]] / [[target|alias]] / [[target#heading]] / ![[target]] 모두 매칭.
WIKILINK_RE = re.compile(r"!?\[\[([^\]]+)\]\]")


def iter_files(root: Path):
    """제외 디렉토리를 건너뛰며 모든 파일을 순회."""
    for path in root.rglob("*"):
        if any(part in EXCLUDE_DIRS for part in path.relative_to(root).parts):
            continue
        yield path


# -----------------------------------------------------------------------------
# [1] 깨진 심볼릭 링크
# -----------------------------------------------------------------------------
def find_broken_symlinks(root: Path) -> list[str]:
    broken = []
    for path in iter_files(root):
        if path.is_symlink() and not path.exists():
            broken.append(f"{path.relative_to(root)} -> {path.readlink()}")
    return broken


# -----------------------------------------------------------------------------
# MD 수집 + WikiLink 파싱
# -----------------------------------------------------------------------------
def collect_md(root: Path) -> dict[Path, str]:
    return {
        p: p.read_text(encoding="utf-8", errors="replace")
        for p in iter_files(root)
        if p.suffix == ".md" and p.is_file()
    }


def link_target(raw: str) -> str:
    """[[folder/note#heading|alias]] -> 'folder/note' (alias·heading 제거)."""
    return raw.split("|", 1)[0].split("#", 1)[0].strip()


def build_name_index(md_files: dict[Path, str], root: Path):
    """Obsidian 식 해석용 인덱스: basename(소문자) -> {상대경로}, 그리고 경로 집합."""
    by_name: dict[str, set[str]] = {}
    rel_paths: set[str] = set()
    for p in md_files:
        rel = p.relative_to(root).as_posix()
        rel_paths.add(rel)
        rel_paths.add(rel[:-3])  # 확장자 없는 형태도 허용
        by_name.setdefault(p.stem.lower(), set()).add(rel)
    return by_name, rel_paths


def resolve(target: str, by_name, rel_paths) -> bool:
    """WikiLink 대상이 어떤 .md 로 해석되는지."""
    if not target:
        return True  # [[#heading]] 같은 동일 문서 내부 앵커는 검사 제외
    t = target.lstrip("/")
    if "/" in t:  # 경로 지정 링크
        return t in rel_paths or f"{t}.md" in rel_paths
    return t.lower() in by_name  # 파일명 링크 (Obsidian shortest-path)


# -----------------------------------------------------------------------------
# [4] 프론트매터 파싱 (최소 구현 — type, links 만)
# -----------------------------------------------------------------------------
def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    data: dict = {}
    cur_list_key = None
    for line in block.splitlines():
        if not line.strip():
            continue
        if cur_list_key and re.match(r"\s*-\s+", line):
            data[cur_list_key].append(line.split("-", 1)[1].strip())
            continue
        cur_list_key = None
        m = re.match(r"(\w+)\s*:\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if val == "":          # 다음 줄부터 리스트
            data[key] = []
            cur_list_key = key
        elif val.startswith("[") and val.endswith("]"):  # 인라인 리스트
            data[key] = [v.strip().strip("\"'") for v in val[1:-1].split(",") if v.strip()]
        else:
            data[key] = val.strip("\"'")
    return data


# -----------------------------------------------------------------------------
# 검사 실행
# -----------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description="온톨로지/문서 하네스 검증")
    ap.add_argument("--strict", action="store_true", help="고립 노드(orphan)도 실패로 처리")
    args = ap.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    # [1] 심볼릭 링크
    for b in find_broken_symlinks(REPO_ROOT):
        errors.append(f"[심볼릭] 깨진 링크: {b}")

    md_files = collect_md(REPO_ROOT)
    by_name, rel_paths = build_name_index(md_files, REPO_ROOT)

    # 그래프(프론트매터 노드용) + 링크 유무(orphan 판정용)
    nodes: dict[str, dict] = {}        # rel -> frontmatter
    out_links: dict[str, list[str]] = {}
    has_link: dict[str, bool] = {p.relative_to(REPO_ROOT).as_posix(): False for p in md_files}

    for path, text in md_files.items():
        rel = path.relative_to(REPO_ROOT).as_posix()
        fm = parse_frontmatter(text)
        if fm.get("type") in ("hub", "spoke"):
            nodes[rel] = fm
        targets = [link_target(m) for m in WIKILINK_RE.findall(text)]
        out_links[rel] = targets
        for tgt in targets:
            # [2] WikiLink 해석
            if not resolve(tgt, by_name, rel_paths):
                errors.append(f"[WikiLink] {rel}: [[{tgt}]] 해석 불가")
            else:
                has_link[rel] = True
                # 역방향: 대상 노드도 '연결됨'으로 표시 (orphan 완화)
                if "/" not in tgt.lstrip("/"):
                    for r in by_name.get(tgt.lower(), ()):
                        has_link[r] = True

    # [3] 고립 노드
    for rel, linked in has_link.items():
        if not linked:
            warnings.append(f"[고립] {rel}: 들어오거나 나가는 WikiLink 없음")

    # [4] 프론트매터 토폴로지 (선언된 노드에 한해)
    if nodes:
        hubs = [r for r, fm in nodes.items() if fm["type"] == "hub"]
        hub_stems = {Path(h).stem.lower() for h in hubs}
        for rel, fm in nodes.items():
            if fm["type"] != "spoke":
                continue
            for tgt in out_links.get(rel, []):
                stem = Path(tgt).stem.lower()
                # 스포크가 가리키는 대상이 '다른 스포크'면 위반
                resolved = by_name.get(stem, set())
                if stem in hub_stems:
                    continue
                if any(r in nodes and nodes[r]["type"] == "spoke" for r in resolved):
                    errors.append(f"[토폴로지] 스포크 {rel} → 스포크 [[{tgt}]] 직접 링크 (허브 경유 필요)")
        # 순환 참조 (프론트매터 노드 그래프 한정)
        cyc = _find_cycle(nodes, out_links, by_name)
        if cyc:
            errors.append(f"[토폴로지] 순환 참조: {' -> '.join(cyc)}")

    # ---- 리포트 ----
    print(f"스캔: .md {len(md_files)}개 | 토폴로지 노드(type 선언) {len(nodes)}개\n")
    for w in warnings:
        print(f"  ⚠️  {w}")
    for e in errors:
        print(f"  ❌ {e}")

    failed = bool(errors) or (args.strict and bool(warnings))
    if failed:
        print(f"\n실패: 에러 {len(errors)} / 경고 {len(warnings)}")
        return 1
    print(f"\n✅ 통과 (경고 {len(warnings)})")
    return 0


def _find_cycle(nodes, out_links, by_name):
    """프론트매터 노드 그래프에서 순환을 하나 찾으면 경로 반환."""
    adj: dict[str, list[str]] = {}
    for rel in nodes:
        adj[rel] = []
        for tgt in out_links.get(rel, []):
            for r in by_name.get(Path(tgt).stem.lower(), ()):
                if r in nodes:
                    adj[rel].append(r)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {r: WHITE for r in nodes}
    stack: list[str] = []

    def dfs(u):
        color[u] = GRAY
        stack.append(u)
        for v in adj.get(u, ()):
            if color[v] == GRAY:
                return stack[stack.index(v):] + [v]
            if color[v] == WHITE:
                r = dfs(v)
                if r:
                    return r
        stack.pop()
        color[u] = BLACK
        return None

    for r in nodes:
        if color[r] == WHITE:
            c = dfs(r)
            if c:
                return c
    return None


if __name__ == "__main__":
    sys.exit(main())
