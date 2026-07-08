from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Bertram Gilfoyle")

'''
버트람 길포일 (Bertram Gilfoyle)
피드 파이퍼의 시스템 아키텍트. 자칭 사타니스트. 딘에쉬를 만성으로 무시하지만 실력은 팀 최정상급.
서버 인프라 전반을 홀로 관리하며 냉소적인 한마디로 회의 분위기를 압도함.
'''


@mcp.tool("introduce_piper_gilfoyle")
async def introduce_piper_gilfoyle() -> str:
    return "안녕하세요, 파이퍼 시스템 아키텍트 길포일입니다."
