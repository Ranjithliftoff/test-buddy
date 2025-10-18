from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.base import registry
from core.models import AuthorRequest, AuthorResponse, Artifact as ArtifactModel
from db.crud import save_artifacts
from api.deps import get_db

router = APIRouter(tags=["author"])

@router.post("/author", response_model=AuthorResponse)
def author(req: AuthorRequest, db: Session = Depends(get_db)):
    if not req.sid:
        raise HTTPException(status_code=400, detail="sid is required")
    out = registry.get("author").run(req.model_dump())

    # Expect out["artifacts"] like:
    # [
    #   {"kind":"feature","toolchain":"cypress-cucumber","feature_path":"...","feature_text":"..."},
    #   {"kind":"steps","toolchain":"cypress-cucumber","step_path":"...","step_text":"..."}
    # ]
    rows = save_artifacts(db, req.sid, out.get("artifacts", []))

    artifacts = [
        ArtifactModel(
            id=r.id,
            kind=r.kind, toolchain=r.toolchain,
            feature_path=r.feature_path, step_path=r.step_path,
            feature_text=r.feature_text, step_text=r.step_text
        )
        for r in rows
    ]
    return AuthorResponse(sid=req.sid, summary=out.get("summary", "Generated artifacts"), artifacts=artifacts)
