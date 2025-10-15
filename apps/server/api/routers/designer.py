from fastapi import APIRouter

router = APIRouter(prefix="/design", tags=["designer"])


@router.get("/")
async def design_root():
    return {"message": "designer root"}
