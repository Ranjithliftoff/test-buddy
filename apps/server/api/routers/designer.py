from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.base import registry
from core.models import DesignRequest, DesignResponse
from db.crud import add_scenarios
from api.deps import get_db

router = APIRouter()

@router.post("/design", response_model=DesignResponse)
def design(req: DesignRequest, db: Session = Depends(get_db)):
    if not req.sid:
        raise HTTPException(status_code=400, detail="sid is required")
    out = registry.get("designer").run(req.dict())
    add_scenarios(db, session_id=req.sid, titles=out["scenarios"])
    return DesignResponse(**out)
