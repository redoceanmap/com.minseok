from pydantic import BaseModel, Field


class ZazuHornbillSchema(BaseModel):

    id: int = Field(0, description="Hornbill ID")
    name: str = Field("자주 (Zazu)", description="Hornbill's name")
    # 왕실의 공식 전령으로 무파사에게 왕국 상황을 보고하는 파랑새. 에이전트 실행 결과를 상위 레이어로 전달하는 리포터

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 9,
                "name": "Zazu",
            }
        }
    }
