from pydantic import BaseModel
from typing import List, Optional, Literal, Dict, Any

# ---------- your existing (kept, with sid added where needed) ----------

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
    sid: str                         # REQUIRED for persistence
    intake: List[IntakeItem] = []

class DesignRequest(BaseModel):
    sid: str                         # REQUIRED
    outline: Optional[str] = None

class AuthorRequest(BaseModel):
    sid: str                         # REQUIRED
    scenarios: List[str] = []

class ExecuteRequest(BaseModel):
    sid: str                         # REQUIRED
    suite: Literal["smoke","regression","generated"] = "generated"

class CurateRequest(BaseModel):
    sid: str                         # REQUIRED
    run_id: str

class PlanResponse(BaseModel):
    title: str
    bullets: List[str]

# ---------- NEW: standardize the rest of the responses ----------

class DesignResponse(BaseModel):
    title: str
    scenarios: List[str]

class Artifact(BaseModel):
    id: str
    toolchain: Literal["cypress-cucumber"] = "cypress-cucumber"
    feature_path: str
    feature_text: str
    step_path: str
    step_text: str

class AuthorResponse(BaseModel):
    summary: str
    artifacts: List[Artifact]

class ExecuteResponse(BaseModel):
    run_id: str
    summary: Dict[str, Any]  # {total, passed, failed, durationMs, suite}

class CurateResponse(BaseModel):
    run_id: str
    insights: List[Dict[str, Any]]
