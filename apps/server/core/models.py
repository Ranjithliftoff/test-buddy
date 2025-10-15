from pydantic import BaseModel
from typing import List, Optional, Literal, Dict, Any

# ------------------ existing (kept) ------------------

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

# ------------------ additions for Phase 2 ------------------

class DesignResponse(BaseModel):
    """High-level scenarios (Gherkin-like titles) to be authored into feature files."""
    title: str
    scenarios: List[str]  # e.g. ["Login works", "Checkout smoke path"]

class Artifact(BaseModel):
    """Cypress + Cucumber artifacts only."""
    id: str
    toolchain: Literal["cypress-cucumber"] = "cypress-cucumber"
    feature_path: str       # e.g. cypress/e2e/auth/login.feature
    feature_text: str       # .feature content (Gherkin)
    step_path: str          # e.g. cypress/e2e/auth/login.steps.js
    step_text: str          # step definitions

class AuthorResponse(BaseModel):
    summary: str
    artifacts: List[Artifact]

class ExecuteResponse(BaseModel):
    run_id: str
    summary: Dict[str, Any]  # { total, passed, failed, durationMs, suite }

class CurateResponse(BaseModel):
    run_id: str
    insights: List[Dict[str, Any]]  # [{"id":"ins-1","kind":"flaky","text":"..."}]
