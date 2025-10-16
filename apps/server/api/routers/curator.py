from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.base import registry
from core.models import CurateRequest, CurateResponse
from db.crud import add_insights
from api.deps import get_db

router = APIRouter()

@router.post("/curate", response_model=CurateResponse)
def curate(req: CurateRequest, db: Session = Depends(get_db)):
    if not req.sid:
        raise HTTPException(status_code=400, detail="sid is required")
    out = registry.get("curator").run(req.dict())
    add_insights(db, session_id=req.sid, run_id=req.run_id, insights=out["insights"])
    return CurateResponse(**out)
