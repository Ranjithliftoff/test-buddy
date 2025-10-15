from fastapi import APIRouter
from core.base import registry
from core.models import PlanRequest, PlanResponse

router = APIRouter()

@router.post("/plan", response_model=PlanResponse)
def plan(req: PlanRequest):
    out = registry.get("planner").run(req.dict())
    return PlanResponse(sid=req.sid, items=out["items"])
