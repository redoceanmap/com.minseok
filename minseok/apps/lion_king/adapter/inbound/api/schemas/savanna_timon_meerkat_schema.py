from pydantic import BaseModel, Field


class TimonMeerkatSchema(BaseModel):

    id: int = Field(0, description="Meerkat ID")
    name: str = Field("티몬 (Timon)", description="Meerkat's name")
    # 항상 망을 보며 위험을 탐지하는 미어캣. 시스템 외부 환경 모니터링 및 이상 징후 조기 탐지 얼리워닝

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 10,
                "name": "Timon",
            }
        }
    }
