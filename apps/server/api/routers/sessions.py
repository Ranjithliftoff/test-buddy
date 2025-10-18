from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.models import SessionCreate, Decision as DecisionModel
from db.crud import create_session, add_decision, get_session_full
from api.deps import get_db

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("")
def create_or_get_session(payload: SessionCreate, db: Session = Depends(get_db)):
    s = create_session(db, module=payload.module)
    return {"sid": str(s.id), "module": s.module, "status": "active"}

@router.get("/{sid}")
def get_full_session(sid: str, db: Session = Depends(get_db)):
    data = get_session_full(db, sid)
    if not data:
        raise HTTPException(status_code=404, detail="session not found")
    return data

@router.post("/{sid}/decision")
def add_decision_api(sid: str, decision: DecisionModel, db: Session = Depends(get_db)):
    d = add_decision(db, sid, decision.step, decision.accepted, decision.note)
    return {"id": d.id, "ok": True}
