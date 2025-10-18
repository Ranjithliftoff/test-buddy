from fastapi import APIRouter, HTTPException
from core.base import registry
from core.models import CurateRequest

router = APIRouter(tags=["curator"])

@router.post("/curate")
def curate(req: CurateRequest):
    if not req.sid:
        raise HTTPException(status_code=400, detail="sid is required")
    out = registry.get("curator").run(req.model_dump())
    return {"sid": req.sid, "run_id": req.run_id, "insights": out.get("insights", [])}
