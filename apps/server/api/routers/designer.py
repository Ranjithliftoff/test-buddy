from fastapi import APIRouter
from core.base import registry
from core.models import DesignRequest, DesignResponse

router = APIRouter()

@router.post("/design", response_model=DesignResponse)
def design(req: DesignRequest):
    out = registry.get("designer").run(req.dict())
    return DesignResponse(scenarios=out["scenarios"], sid=req.sid)
