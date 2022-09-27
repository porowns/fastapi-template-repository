from fastapi import APIRouter

router = APIRouter(prefix="/readyz")


@router.get("")
async def readyz():
    return {"status": "OK"}
