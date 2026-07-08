from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Nelson Bighetti")

'''
넬슨 비게티 (Nelson Bighetti / Big Head)
리차드의 어린 시절 친구. 피드 파이퍼를 떠나 Hooli에 입사했다가 
우연히 Hooli XYZ 사장까지 됨.
특별히 노력하지 않아도 좋은 자리에 앉게 되는 기이한 행운의 소유자.
'''


@mcp.tool("introduce_piper_bighetti")
async def introduce_piper_bighetti() -> str:
    return "안녕하세요, 파이퍼 HR 빅헤드 비게티입니다."
