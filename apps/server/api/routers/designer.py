# apps/server/api/routers/designer.py
from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from db.base import SessionLocal
from db import models as m
from api.models import DesignRequest, DesignResponse
from core.services.designer_service import DesignerAgent

router = APIRouter(prefix="/design", tags=["designer"])
designer = DesignerAgent()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "",
    response_model=DesignResponse,
    summary="Generate scenario outlines (transient; not persisted)"
)
def create_design(
    req: DesignRequest,
    x_session_id: str = Header(..., alias="X-Session-Id"),
    db: Session = Depends(get_db),
):
    # Validate session id header
    try:
        sid = UUID(x_session_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid X-Session-Id UUID")

    # Ensure session exists
    sess = db.query(m.Session).filter(m.Session.id == sid).first()
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")

    # Use the latest plan's bullets (if present)
    last_plan = (
        db.query(m.Plan)
        .filter(m.Plan.session_id == sid)
        .order_by(m.Plan.id.desc())
        .first()
    )
    bullets = (last_plan.bullets or {}).get("bullets", []) if last_plan else []

    # Generate scenarios (no persistence)
    result = designer.design(bullets, req.outline)

    return DesignResponse(scenarios=result.get("scenarios", []))
