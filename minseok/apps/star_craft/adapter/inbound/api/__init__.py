from __future__ import annotations

# star_craft_router는 main.py에서 처음 접근할 때 지연 생성됩니다. (PEP 562)

_star_craft_router = None


def __getattr__(name: str):
    global _star_craft_router

    if name == "star_craft_router":
        if _star_craft_router is None:
            _star_craft_router = _build_star_craft_router()
        return _star_craft_router

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def _build_star_craft_router():
    from fastapi import APIRouter

    from star_craft.adapter.inbound.api.v1.email_request_router import email_request_router

    router = APIRouter(prefix="/star_craft", tags=["star_craft"])
    router.include_router(email_request_router)
    return router
