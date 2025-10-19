# apps/server/api/routers/planner.py
from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from db.base import SessionLocal
from db import models as m
from db.crud import add_plan
from api.models import PlanRequest, PlanResponse
from core.services.planner_service import PlannerAgent

router = APIRouter(prefix="/plan", tags=["planner"])
planner = PlannerAgent()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=PlanResponse, summary="Generate a test plan and persist it")
def create_plan(
    req: PlanRequest,
    x_session_id: str = Header(..., alias="X-Session-Id"),
    db: Session = Depends(get_db)
):
    """Generate a test plan using the PlannerAgent and save it in the database."""
    try:
        sid = UUID(x_session_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid X-Session-Id UUID")

    # Validate session exists
    sess = db.query(m.Session).filter(m.Session.id == sid).first()
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")

    # Run AI planner
    result = planner.plan(req.intake)
    add_plan(db, sid, result["title"], result["bullets"])

    return PlanResponse(title=result["title"], bullets=result["bullets"])
