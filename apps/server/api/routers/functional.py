from fastapi import APIRouter
from typing import List, Literal, Dict, Any

router = APIRouter()

@router.get("/functional/test")
def functional_test() -> Dict[str, Any]:
    """Return a small, structured payload to prove BE→FE flow."""
    return {
        "module": "functional",
        "summary": {"total": 3, "passed": 2, "failed": 1},
        "tests": [
            {"id": 1, "name": "Login page loads", "status": "passed"},
            {"id": 2, "name": "Submit form with valid data", "status": "passed"},
            {"id": 3, "name": "Submit form with invalid data", "status": "failed"},
        ],
    }

@router.post("/functional/plan")
def functional_plan(payload: dict) -> Dict[str, Any]:
    """
    Accept a minimal intake payload and echo a draft 'plan'.
    Example payload:
    { "mode": "web", "url": "https://example.com" }
    """
    mode = payload.get("mode", "web")
    url = payload.get("url", "")
    return {
        "module": "functional",
        "intake": {"mode": mode, "url": url},
        "plan": {
            "title": "Functional Test Plan (Draft)",
            "bullets": [
                "Crawl landing and auth pages",
                "Identify primary user journeys",
                "Generate candidate scenarios for form validations",
            ],
        },
    }
