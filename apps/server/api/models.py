# apps/server/api/models.py
from pydantic import BaseModel
from typing import List, Optional, Literal, Dict, Any

class SessionCreate(BaseModel):
    module: Literal["uiux","functional","api","smoke","regression"] = "functional"

class IntakeItem(BaseModel):
    kind: Literal["figma","web","doc","sheet"]
    url: Optional[str] = None
    note: Optional[str] = None

class Decision(BaseModel):
    step: Literal["planner","designer","author","executor","curator"]
    accepted: bool
    note: Optional[str] = None

class PlanRequest(BaseModel):
    intake: List[IntakeItem] = []

class DesignRequest(BaseModel):
    outline: Optional[str] = None

class AuthorRequest(BaseModel):
    scenarios: List[str] = []

class ExecuteRequest(BaseModel):
    suite: Literal["smoke","regression","generated"] = "generated"

class CurateRequest(BaseModel):
    run_id: str

class PlanResponse(BaseModel):
    title: str
    bullets: List[str]
