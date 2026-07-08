from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Dinesh Chugtai")

'''
딘에쉬 추그타이 (Dinesh Chugtai)
피드 파이퍼의 백엔드 개발자. 길포일과 끊임없이 티격태격하지만 실력은 충분함.
잠깐 CEO 자리에 앉기도 했으나 처참한 결과로 끝남. 대시보드 개발 담당.
'''


@mcp.tool("introduce_piper_dinesh")
async def introduce_piper_dinesh() -> str:
    return "안녕하세요, 파이퍼 대시보드 개발자 딘에쉬입니다."
