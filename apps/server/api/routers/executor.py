from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.base import registry
from core.models import ExecuteRequest, ExecuteResponse
from db.crud import add_run
from api.deps import get_db

router = APIRouter()

@router.post("/execute", response_model=ExecuteResponse)
def execute(req: ExecuteRequest, db: Session = Depends(get_db)):
    if not req.sid:
        raise HTTPException(status_code=400, detail="sid is required")
    out = registry.get("executor").run(req.dict())
    add_run(db, session_id=req.sid, summary=out["summary"])
    return ExecuteResponse(**out)
