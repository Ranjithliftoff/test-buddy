from fastapi import APIRouter

router = APIRouter(prefix="/execute", tags=["executor"])


@router.get("/logs")
async def exec_logs():
    return {"logs": []}
