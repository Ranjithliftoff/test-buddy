# apps/server/api/routers/sessions.py
from __future__ import annotations

from uuid import UUID, uuid4
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.base import SessionLocal
from db import models as m  # SQLAlchemy models
# Pydantic request models (the ones you showed earlier)
# SessionCreate(module=...), Decision(step/accepted/note)
from ..models import SessionCreate, Decision as DecisionIn


router = APIRouter(prefix="/sessions", tags=["sessions"])


# --- DB session dependency ----------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Helpers ------------------------------------------------------------------
def _ensure_uuid(value: str) -> UUID:
    try:
        return UUID(value)
    except Exception:
        raise HTTPException(status_code=400, detail="sid must be a valid UUID")

def _serialize_session(s: m.Session) -> Dict[str, Any]:
    """Return a consistent JSON-friendly shape for a session."""
    return {
        "id": str(s.id),
        "created_at": s.created_at.isoformat() if s.created_at else None,
        "module": s.module,
        "plans": [
            {
                "id": p.id,
                "title": p.title,
                "bullets": p.bullets,  # JSONB
            }
            for p in (s.plans or [])
        ],
        "decisions": [
            {
                "id": d.id,
                "step": d.step,
                "accepted": d.accepted,
                "note": d.note,
            }
            for d in (s.decisions or [])
        ],
        "artifacts": [
            {
                "id": a.id,
                "kind": a.kind,
                "toolchain": a.toolchain,
                "feature_path": a.feature_path,
                "step_path": a.step_path,
                "feature_text": a.feature_text,
                "step_text": a.step_text,
            }
            for a in (s.artifacts or [])
        ],
        "runs": [
            {
                "id": r.id,
                "suite": r.suite,
                "status": r.status,
                "summary": r.summary,
            }
            for r in (s.runs or [])
        ],
    }


# --- Routes -------------------------------------------------------------------
@router.post("", summary="Create or get session")
def create_or_get_session(req: SessionCreate, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Creates a new session row with the requested module and returns its id.
    (If you ever want idempotency, you can add a lookup by some external key.)
    """
    try:
        s = m.Session(id=uuid4(), module=req.module)
        db.add(s)
        db.commit()
        db.refresh(s)
        return {"id": str(s.id), "module": s.module, "created_at": s.created_at.isoformat()}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal error creating session: {e}")


@router.get("/{sid}", summary="Get full session")
def get_full_session(sid: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Loads a session and all related rows (plans, decisions, artifacts, runs).
    Raises 404 if the session does not exist, and returns clear error text if
    the sid is malformed.
    """
    _sid = _ensure_uuid(sid)
    try:
        session_obj = (
            db.query(m.Session)
            .filter(m.Session.id == _sid)
            .first()
        )
        if not session_obj:
            raise HTTPException(status_code=404, detail="session not found")
        return _serialize_session(session_obj)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error loading session: {e}")


@router.post("/{sid}/decision", summary="Add decision API")
def add_decision(sid: str, req: DecisionIn, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Attaches a decision row to the given session id.
    """
    _sid = _ensure_uuid(sid)
    try:
        session_obj = db.query(m.Session).filter(m.Session.id == _sid).first()
        if not session_obj:
            raise HTTPException(status_code=404, detail="session not found")

        dec = m.Decision(
            session_id=session_obj.id,
            step=req.step,
            accepted=req.accepted,
            note=req.note,
        )
        db.add(dec)
        db.commit()
        db.refresh(dec)
        return {
            "ok": True,
            "decision": {
                "id": dec.id,
                "step": dec.step,
                "accepted": dec.accepted,
                "note": dec.note,
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal error adding decision: {e}")
