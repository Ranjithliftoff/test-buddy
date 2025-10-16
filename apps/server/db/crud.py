from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from . import models as m

def get_or_create_session(db: Session, module: str, source_type: Optional[str]=None,
                          source_url: Optional[str]=None, notes: Optional[str]=None) -> m.Session:
    q = db.query(m.Session).filter(m.Session.module==module, m.Session.status=="active")
    s = q.first()
    if s:
        return s
    s = m.Session(module=module, source_type=source_type, source_url=source_url, notes=notes)
    db.add(s); db.commit(); db.refresh(s)
    return s

def add_plan(db: Session, session_id, title: str, bullets: List[str]) -> m.Plan:
    p = m.Plan(session_id=session_id, title=title, bullets=bullets)
    db.add(p); db.commit(); db.refresh(p); return p

def add_scenarios(db: Session, session_id, titles: List[str]) -> List[m.Scenario]:
    rows = [m.Scenario(session_id=session_id, title=t) for t in titles]
    db.add_all(rows); db.commit()
    for r in rows: db.refresh(r)
    return rows

def add_artifacts(db: Session, session_id, artifacts: List[Dict[str, Any]]) -> List[m.Artifact]:
    rows = [m.Artifact(session_id=session_id, **a) for a in artifacts]
    db.add_all(rows); db.commit()
    for r in rows: db.refresh(r)
    return rows

def add_run(db: Session, session_id, summary: Dict[str, Any]) -> m.Run:
    r = m.Run(session_id=session_id, summary=summary)
    db.add(r); db.commit(); db.refresh(r); return r

def add_insights(db: Session, session_id, run_id, insights: List[Dict[str, Any]]) -> List[m.Insight]:
    rows = [m.Insight(session_id=session_id, run_id=run_id, kind=i["kind"], text=i["text"]) for i in insights]
    db.add_all(rows); db.commit()
    for r in rows: db.refresh(r)
    return rows

def add_decision(db: Session, session_id, step: str, accepted: bool, note: Optional[str]) -> m.Decision:
    d = m.Decision(session_id=session_id, step=step, accepted=accepted, note=note)
    db.add(d); db.commit(); db.refresh(d); return d

def get_session_full(db: Session, session_id):
    s = db.query(m.Session).filter_by(id=session_id).first()
    if not s:
        return None
    return {
        "id": str(s.id),
        "module": s.module,
        "source_type": s.source_type,
        "source_url": s.source_url,
        "status": s.status,
        "plans": [{"id": str(p.id), "title": p.title, "bullets": p.bullets, "created_at": str(p.created_at)} for p in s.plans],
        "scenarios": [{"id": str(x.id), "title": x.title, "created_at": str(x.created_at)} for x in s.scenarios],
        "artifacts": [{"id": str(a.id), "toolchain": a.toolchain, "feature_path": a.feature_path, "step_path": a.step_path} for a in s.artifacts],
        "runs": [{"id": str(r.id), "summary": r.summary, "created_at": str(r.created_at)} for r in s.runs],
        "insights": [{"id": str(i.id), "kind": i.kind, "text": i.text, "created_at": str(i.created_at)} for i in s.insights],
        "decisions": [{"id": str(d.id), "step": d.step, "accepted": d.accepted, "note": d.note, "created_at": str(d.created_at)} for d in s.decisions],
    }
