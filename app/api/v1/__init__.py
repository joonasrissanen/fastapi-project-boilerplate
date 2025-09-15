from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.polls import router as polls_router

router = APIRouter(prefix="/v1")

router.include_router(health_router)
router.include_router(polls_router)
