# apps/server/db/crud.py
from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional, Union

from sqlalchemy.orm import Session

from . import models as m


# -------- utilities --------
def _to_uuid(v: Union[str, uuid.UUID]) -> uuid.UUID:
    if isinstance(v, uuid.UUID):
        return v
    return uuid.UUID(str(v))


# -------- sessions --------
def get_or_create_session(db: Session, module: str) -> m.Session:
    s = m.Session(module=module)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


def get_session(db: Session, sid: Union[str, uuid.UUID]) -> Optional[m.Session]:
    try:
        uid = _to_uuid(sid)
    except Exception:
        return None
    return db.query(m.Session).filter(m.Session.id == uid).first()


def get_session_full(db: Session, sid: Union[str, uuid.UUID]):
    """
    Return ORM objects so routers can shape the response:
      {"session": Session, "decisions":[...], "plans":[...], "artifacts":[...], "runs":[...]}
    """
    sess = get_session(db, sid)
    if not sess:
        return None
    uid = _to_uuid(sid)

    decisions = (
        db.query(m.Decision)
        .filter(m.Decision.session_id == uid)
        .order_by(m.Decision.id.asc())
        .all()
    )
    plans = (
        db.query(m.Plan)
        .filter(m.Plan.session_id == uid)
        .order_by(m.Plan.id.asc())
        .all()
    )
    arts = (
        db.query(m.Artifact)
        .filter(m.Artifact.session_id == uid)
        .order_by(m.Artifact.id.asc())
        .all()
    )
    runs = (
        db.query(m.Run)
        .filter(m.Run.session_id == uid)
        .order_by(m.Run.id.asc())
        .all()
    )

    return {"session": sess, "decisions": decisions, "plans": plans, "artifacts": arts, "runs": runs}


# -------- decisions --------
def add_decision(
    db: Session,
    session_id: Union[str, uuid.UUID],
    step: str,
    accepted: bool,
    note: Optional[str],
) -> m.Decision:
    uid = _to_uuid(session_id)
    d = m.Decision(session_id=uid, step=step, accepted=accepted, note=note)
    db.add(d)
    db.commit()
    db.refresh(d)
    return d


# -------- plans --------
def add_plan(
    db: Session,
    session_id: Union[str, uuid.UUID],
    title: str,
    bullets: List[str],
) -> m.Plan:
    uid = _to_uuid(session_id)
    row = m.Plan(session_id=uid, title=title, bullets={"bullets": bullets})
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


# Back-compat wrapper (used by older code)
def save_plan(db: Session, sid: str, title: str, bullets: List[str]) -> m.Plan:
    return add_plan(db, sid, title, bullets)


# -------- artifacts --------
def add_artifact_feature(
    db: Session,
    session_id: Union[str, uuid.UUID],
    feature_path: str,
    feature_text: str,
) -> m.Artifact:
    uid = _to_uuid(session_id)
    row = m.Artifact(
        session_id=uid,
        kind="feature",
        toolchain="cypress-cucumber",
        feature_path=feature_path,
        feature_text=feature_text,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def add_artifact_steps(
    db: Session,
    session_id: Union[str, uuid.UUID],
    step_path: str,
    step_text: str,
) -> m.Artifact:
    uid = _to_uuid(session_id)
    row = m.Artifact(
        session_id=uid,
        kind="steps",
        toolchain="cypress-cucumber",
        step_path=step_path,
        step_text=step_text,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


# Back-compat wrapper (accepts a list of artifact dicts)
def save_artifacts(db: Session, sid: str, artifacts: List[Dict[str, Any]]) -> List[m.Artifact]:
    uid = _to_uuid(sid)
    out: List[m.Artifact] = []
    for a in artifacts or []:
        kind = (a.get("kind") or "feature").lower()
        if kind == "steps":
            out.append(
                add_artifact_steps(
                    db,
                    uid,
                    a.get("step_path") or "",
                    a.get("step_text") or "",
                )
            )
        else:
            out.append(
                add_artifact_feature(
                    db,
                    uid,
                    a.get("feature_path") or "",
                    a.get("feature_text") or "",
                )
            )
    return out


# -------- runs --------
def save_run(
    db: Session,
    sid: Union[str, uuid.UUID],
    suite: str,
    status: str,
    summary: Dict[str, Any],
) -> m.Run:
    uid = _to_uuid(sid)
    r = m.Run(session_id=uid, suite=suite, status=status, summary=summary or {})
    db.add(r)
    db.commit()
    db.refresh(r)
    return r
