from fastapi import APIRouter

router = APIRouter(prefix="/author", tags=["author"])


@router.get("/")
async def author_root():
    return {"message": "author root"}
