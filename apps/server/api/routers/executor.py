from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.base import registry
from core.models import ExecuteRequest, ExecuteResponse
from db.crud import save_run
from api.deps import get_db

router = APIRouter(tags=["executor"])

@router.post("/execute", response_model=ExecuteResponse)
def execute(req: ExecuteRequest, db: Session = Depends(get_db)):
    if not req.sid:
        raise HTTPException(status_code=400, detail="sid is required")
    out = registry.get("executor").run(req.model_dump())
    summary = out.get("summary", {})
    run = save_run(db, req.sid, suite=req.suite, status=summary.get("status", "passed"), summary=summary)
    return ExecuteResponse(sid=req.sid, run_id=str(run.id), suite=req.suite, summary=summary)
