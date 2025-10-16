from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.base import registry
from core.models import AuthorRequest, AuthorResponse
from db.crud import add_artifacts
from api.deps import get_db

router = APIRouter()

@router.post("/author", response_model=AuthorResponse)
def author(req: AuthorRequest, db: Session = Depends(get_db)):
    if not req.sid:
        raise HTTPException(status_code=400, detail="sid is required")
    out = registry.get("author").run(req.dict())
    add_artifacts(db, session_id=req.sid, artifacts=out["artifacts"])
    return AuthorResponse(**out)
