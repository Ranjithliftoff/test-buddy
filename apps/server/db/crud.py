# apps/server/db/crud.py
from typing import Optional
import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from .base import SessionLocal
from . import models as m

# --- Session helpers ---
def get_db() -> Session:
    return SessionLocal()

def get_or_create_session(db: Session, module: str) -> m.Session:
    # Re-use latest open session for same module in last hour if you want; simple create for now.
    new_sess = m.Session(module=module)
    db.add(new_sess)
    db.commit()
    db.refresh(new_sess)
    return new_sess

def get_session(db: Session, sid: uuid.UUID) -> Optional[m.Session]:
    return db.get(m.Session, sid)

# --- Decision ---
def add_decision(db: Session, sid: uuid.UUID, step: str, accepted: bool, note: Optional[str]) -> m.Decision:
    dec = m.Decision(session_id=sid, step=step, accepted=accepted, note=note)
    db.add(dec)
    db.commit()
    db.refresh(dec)
    return dec

# --- Plan ---
def save_plan(db: Session, sid: uuid.UUID, title: str, bullets: list[str]) -> m.Plan:
    plan = m.Plan(session_id=sid, title=title, bullets={"bullets": bullets})
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan

# --- Artifacts (feature + steps text) ---
def save_artifact(
    db: Session,
    sid: uuid.UUID,
    kind: str,
    toolchain: str,
    feature_path: Optional[str],
    step_path: Optional[str],
    feature_text: Optional[str],
    step_text: Optional[str],
) -> m.Artifact:
    art = m.Artifact(
        session_id=sid,
        kind=kind,
        toolchain=toolchain,
        feature_path=feature_path,
        step_path=step_path,
        feature_text=feature_text,
        step_text=step_text,
    )
    db.add(art)
    db.commit()
    db.refresh(art)
    return art

# --- Runs ---
def save_run(db: Session, sid: uuid.UUID, suite: str, status: str, summary: Optional[dict]) -> m.Run:
    run = m.Run(session_id=sid, suite=suite, status=status, summary=summary or {})
    db.add(run)
    db.commit()
    db.refresh(run)
    return run

def get_session_full(db: Session, sid: uuid.UUID) -> dict:
    sess = db.get(m.Session, sid)
    if not sess:
        return {}
    return {
        "id": str(sess.id),
        "module": sess.module,
        "created_at": sess.created_at.isoformat(),
        "decisions": [
            {"id": d.id, "step": d.step, "accepted": d.accepted, "note": d.note}
            for d in sess.decisions
        ],
        "plans": [
            {"id": p.id, "title": p.title, "bullets": p.bullets.get("bullets", [])}
            for p in sess.plans
        ],
        "artifacts": [
            {
                "id": a.id,
                "kind": a.kind,
                "toolchain": a.toolchain,
                "feature_path": a.feature_path,
                "step_path": a.step_path,
            }
            for a in sess.artifacts
        ],
        "runs": [
            {"id": r.id, "suite": r.suite, "status": r.status, "summary": r.summary}
            for r in sess.runs
        ],
    }
