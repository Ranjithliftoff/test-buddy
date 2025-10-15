from fastapi import APIRouter
from core.base import registry
from core.models import CurateRequest, CurateResponse

router = APIRouter()

@router.post("/curate", response_model=CurateResponse)
def curate(req: CurateRequest):
    out = registry.get("curator").run(req.dict())
    return CurateResponse(**out)
