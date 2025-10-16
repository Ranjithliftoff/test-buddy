from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.models import SessionCreate, Decision as DecisionModel
from db.crud import get_or_create_session, add_decision, get_session_full
from api.deps import get_db

router = APIRouter()

@router.post("/sessions")
def create_or_get_session(payload: SessionCreate, db: Session = Depends(get_db)):
    s = get_or_create_session(db, module=payload.module)
    return {"id": str(s.id), "module": s.module, "status": s.status}

@router.get("/sessions/{sid}")
def get_session(sid: str, db: Session = Depends(get_db)):
    data = get_session_full(db, sid)
    return data or {"error": "not found"}

@router.post("/sessions/{sid}/decision")
def add_decision_api(sid: str, decision: DecisionModel, db: Session = Depends(get_db)):
    d = add_decision(db, sid, decision.step, decision.accepted, decision.note)
    return {"id": str(d.id), "ok": True}
