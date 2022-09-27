from . import health
from . import ready
from fastapi import APIRouter

router = APIRouter(prefix="/v1")
router.include_router(router=health.router)
router.include_router(router=ready.router)
