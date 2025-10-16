from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.base import registry
from core.models import PlanRequest, PlanResponse
from db.crud import add_plan
from api.deps import get_db

router = APIRouter()

@router.post("/plan", response_model=PlanResponse)
def plan(req: PlanRequest, db: Session = Depends(get_db)):
    if not req.sid:
        raise HTTPException(status_code=400, detail="sid is required")
    out = registry.get("planner").run(req.dict())
    add_plan(db, session_id=req.sid, title=out["title"], bullets=out["bullets"])
    return PlanResponse(**out)
