from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.base import registry
from core.models import PlanRequest, PlanResponse
from db.crud import save_plan
from api.deps import get_db

router = APIRouter(tags=["planner"])

@router.post("/plan", response_model=PlanResponse)
def plan(req: PlanRequest, db: Session = Depends(get_db)):
    if not req.sid:
        raise HTTPException(status_code=400, detail="sid is required")
    out = registry.get("planner").run(req.model_dump())
    # expect agent returns {"sid":..., "title":..., "bullets":[...]} or at least title/bullets
    sid = req.sid
    title = out.get("title", "Plan")
    bullets = out.get("bullets", [])
    row = save_plan(db, sid, title, bullets)
    return PlanResponse(sid=sid, title=title, bullets=bullets, plan_id=row.id)
