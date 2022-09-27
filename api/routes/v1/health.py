from fastapi import APIRouter

router = APIRouter(prefix="/healthz")


@router.get("")
async def healthz():
    return {"status": "OK"}
