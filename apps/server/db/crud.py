# apps/server/db/crud.py
import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from . import models as m

# ---- Sessions ----
def create_session(db: Session, module: str) -> m.Session:
    """Create a new session for the given test module."""
    s = m.Session(module=module)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


def get_session(db: Session, sid: str) -> Optional[m.Session]:
    """Retrieve a session by UUID string (safe conversion)."""
    try:
        uid = uuid.UUID(sid)
    except Exception:
        return None
    return db.get(m.Session, uid)


# ---- Decisions ----
def add_decision(db: Session, sid: str, step: str, accepted: bool, note: Optional[str]) -> m.Decision:
    """Persist a decision (approve/reject step)."""
    uid = uuid.UUID(sid)
    d = m.Decision(session_id=uid, step=step, accepted=accepted, note=note)
    db.add(d)
    db.commit()
    db.refresh(d)
    return d


# ---- Plans ----
def save_plan(db: Session, sid: str, title: str, bullets: List[str]) -> m.Plan:
    """Save a generated plan for a session."""
    uid = uuid.UUID(sid)
    p = m.Plan(session_id=uid, title=title, bullets={"bullets": bullets})
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


# ---- Artifacts ----
def save_artifacts(db: Session, sid: str, artifacts: List[Dict[str, Any]]) -> List[m.Artifact]:
    """Save feature/step artifacts for a session."""
    uid = uuid.UUID(sid)
    rows: List[m.Artifact] = []
    for a in artifacts:
        row = m.Artifact(
            session_id=uid,
            kind=a.get("kind", "feature"),
            toolchain=a.get("toolchain", "cypress-cucumber"),
            feature_path=a.get("feature_path"),
            step_path=a.get("step_path"),
            feature_text=a.get("feature_text"),
            step_text=a.get("step_text"),
        )
        db.add(row)
        rows.append(row)
    db.commit()
    for r in rows:
        db.refresh(r)
    return rows


# ---- Runs ----
def save_run(db: Session, sid: str, suite: str, status: str, summary: Dict[str, Any]) -> m.Run:
    """Record a run summary (e.g., test execution results)."""
    uid = uuid.UUID(sid)
    r = m.Run(session_id=uid, suite=suite, status=status, summary=summary or {})
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


# ---- Session aggregate ----
def get_session_full(db: Session, sid: str) -> Optional[Dict[str, Any]]:
    """Return full snapshot of a session including plans, artifacts, runs, decisions."""
    s = get_session(db, sid)
    if not s:
        return None

    return {
        "id": str(s.id),
        "module": s.module,
        "created_at": s.created_at.isoformat(),
        "plans": [
            {
                "id": p.id,
                "title": p.title,
                "bullets": (p.bullets or {}).get("bullets", []),
                "created_at": p.created_at.isoformat(),
            }
            for p in s.plans
        ],
        "artifacts": [
            {
                "id": a.id,
                "kind": a.kind,
                "toolchain": a.toolchain,
                "feature_path": a.feature_path,
                "step_path": a.step_path,
                "created_at": a.created_at.isoformat(),
            }
            for a in s.artifacts
        ],
        "runs": [
            {
                "id": r.id,
                "suite": r.suite,
                "status": r.status,
                "summary": r.summary or {},
                "created_at": r.created_at.isoformat(),
            }
            for r in s.runs
        ],
        "decisions": [
            {
                "id": d.id,
                "step": d.step,
                "accepted": d.accepted,
                "note": d.note,
                "created_at": d.created_at.isoformat(),
            }
            for d in s.decisions
        ],
    }
