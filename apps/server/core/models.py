from pydantic import BaseModel
from typing import List, Optional, Literal, Dict, Any

# ----- Request models (sid REQUIRED for persistence) -----
class SessionCreate(BaseModel):
    module: Literal["uiux", "functional", "api", "smoke", "regression"] = "functional"

class IntakeItem(BaseModel):
    kind: Literal["figma", "web", "doc", "sheet"]
    url: Optional[str] = None
    note: Optional[str] = None

class Decision(BaseModel):
    step: Literal["planner", "designer", "author", "executor", "curator"]
    accepted: bool
    note: Optional[str] = None

class PlanRequest(BaseModel):
    sid: str
    intake: List[IntakeItem] = []

class DesignRequest(BaseModel):
    sid: str
    outline: Optional[str] = None

class AuthorRequest(BaseModel):
    sid: str
    scenarios: List[str] = []

class ExecuteRequest(BaseModel):
    sid: str
    suite: Literal["smoke", "regression", "generated"] = "generated"

class CurateRequest(BaseModel):
    sid: str
    run_id: str

# ----- Response models -----
class PlanResponse(BaseModel):
    sid: Optional[str] = None
    title: str
    bullets: List[str]
    plan_id: Optional[int] = None

class DesignResponse(BaseModel):
    sid: Optional[str] = None
    title: str
    scenarios: List[str]

class Artifact(BaseModel):
    id: int
    kind: Literal["feature", "steps", "asset"] = "feature"
    toolchain: Literal["cypress-cucumber"] = "cypress-cucumber"
    feature_path: Optional[str] = None
    step_path: Optional[str] = None
    feature_text: Optional[str] = None
    step_text: Optional[str] = None

class AuthorResponse(BaseModel):
    sid: Optional[str] = None
    summary: str
    artifacts: List[Artifact]

class ExecuteResponse(BaseModel):
    sid: Optional[str] = None
    run_id: str
    suite: str
    summary: Dict[str, Any]
