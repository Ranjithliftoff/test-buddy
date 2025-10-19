# apps/server/api/models.py
from pydantic import BaseModel
from typing import List, Optional, Literal, Dict, Any

# --- Core Session ---
class SessionCreate(BaseModel):
    module: Literal["uiux", "functional", "api", "smoke", "regression"] = "functional"

# --- Planner ---
class IntakeItem(BaseModel):
    kind: Literal["figma", "web", "doc", "sheet"]
    url: Optional[str] = None
    note: Optional[str] = None

class PlanRequest(BaseModel):
    intake: List[IntakeItem] = []

class PlanResponse(BaseModel):
    title: str
    bullets: List[str]

# --- Designer ---
class DesignRequest(BaseModel):
    outline: Optional[str] = None

# --- Author ---
class AuthorRequest(BaseModel):
    scenarios: List[str] = []

# --- Executor ---
class ExecuteRequest(BaseModel):
    suite: Literal["smoke", "regression", "generated"] = "generated"

# --- Curator ---
class CurateRequest(BaseModel):
    run_id: str

# --- Decision ---
class Decision(BaseModel):
    step: Literal["planner", "designer", "author", "executor", "curator"]
    accepted: bool
    note: Optional[str] = None
