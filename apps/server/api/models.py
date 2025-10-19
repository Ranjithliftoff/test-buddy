# apps/server/api/models.py
from __future__ import annotations
from typing import Any, Dict, List, Optional, Literal
from pydantic import BaseModel

# --- sessions ---
class SessionCreate(BaseModel):
    module: Literal["uiux", "functional", "api", "smoke", "regression"] = "functional"

# --- planner ---
class IntakeItem(BaseModel):
    kind: Literal["figma", "web", "doc", "sheet"]
    url: Optional[str] = None
    note: Optional[str] = None

class PlanRequest(BaseModel):
    intake: List[IntakeItem] = []

class PlanResponse(BaseModel):
    title: str
    bullets: List[str]

# --- designer ---
class DesignRequest(BaseModel):
    outline: Optional[str] = None

class DesignResponse(BaseModel):
    scenarios: List[Dict[str, Any]]

# --- author ---
class AuthorRequest(BaseModel):
    # Allow strings (scenario names) or full objects. Router will normalize.
    scenarios: List[Any] = []

class AuthorResponse(BaseModel):
    feature: Dict[str, str]   # {path, text}
    steps: Dict[str, str]     # {path, text}

# --- decisions ---
class Decision(BaseModel):
    step: Literal["planner", "designer", "author", "executor", "curator"]
    accepted: bool
    note: Optional[str] = None
