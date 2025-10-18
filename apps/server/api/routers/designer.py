from fastapi import APIRouter, HTTPException
from core.base import registry
from core.models import DesignRequest, DesignResponse

router = APIRouter(tags=["designer"])

@router.post("/design", response_model=DesignResponse)
def design(req: DesignRequest):
    if not req.sid:
        raise HTTPException(status_code=400, detail="sid is required")
    out = registry.get("designer").run(req.model_dump())
    return DesignResponse(sid=req.sid, title=out.get("title", "Design"), scenarios=out.get("scenarios", []))
