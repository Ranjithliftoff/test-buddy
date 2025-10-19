# apps/server/api/routers/author.py
from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from db.base import SessionLocal
from db import models as m
from db.crud import add_artifact_feature, add_artifact_steps
from api.models import AuthorRequest, AuthorResponse
from core.services.author_service import AuthorAgent

router = APIRouter(prefix="/author", tags=["author"])
author = AuthorAgent()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "",
    response_model=AuthorResponse,
    summary="Generate and persist feature & step artifacts"
)
def create_artifacts(
    req: AuthorRequest,
    x_session_id: str = Header(..., alias="X-Session-Id"),
    db: Session = Depends(get_db)
):
    # Validate session ID
    try:
        sid = UUID(x_session_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid X-Session-Id UUID")

    # Confirm session exists
    sess = db.query(m.Session).filter(m.Session.id == sid).first()
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")

    # Normalize scenarios: accept either strings or dicts
    scenarios = []
    for s in (req.scenarios or []):
        if isinstance(s, str):
            scenarios.append({
                "name": s,
                "tags": [],
                "given": ["I am on the app"],
                "when": ["I perform an action"],
                "then": ["I see the expected result"],
            })
        else:
            scenarios.append(s)

    # Run Author agent
    result = author.author(scenarios)
    feature = result["feature"]
    steps = result["steps"]

    # Persist generated artifacts
    add_artifact_feature(db, sid, feature["path"], feature["text"])
    add_artifact_steps(db, sid, steps["path"], steps["text"])

    # Return structured response
    return AuthorResponse(feature=feature, steps=steps)
