from fastapi import APIRouter

router = APIRouter(prefix="/curate", tags=["curator"])


@router.get("/")
async def curate_root():
    return {"message": "curator root"}
