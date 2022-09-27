from fastapi import APIRouter
from api.routes import v1

router = APIRouter()

router.include_router(v1.router)
