from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Jared Dunn")

'''
재러드 던 (Jared Dunn)
피드 파이퍼의 COO. 원래 Hooli에서 개빈 벨슨의 비서로 근무했으나 방치된 컨테이너 배에서 발견됨.
기묘한 이력과 달리 회사 운영에 대한 열정은 최상급. 팀의 정서적 지주 역할.
'''


@mcp.tool("introduce_piper_dunn")
async def introduce_piper_dunn() -> str:
    return "안녕하세요, 파이퍼 COO 재러드 던입니다."
