from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Literal, Dict, Any
from urllib.parse import urlparse

router = APIRouter()

class AnalyzeReq(BaseModel):
    source: Literal["figma", "web"] = "web"
    url: str

@router.post("/uiux/analyze")
def uiux_analyze(req: AnalyzeReq) -> Dict[str, Any]:
    """
    Mock analysis: returns components + basic heuristic issues for figma/web URLs.
    Later we’ll plug real parsers; for Phase 2 we return stable, structured data.
    """
    parsed = urlparse(req.url or "")
    host = parsed.netloc or "example.com"

    components = [
        {"name": "Header", "type": "layout", "notes": "Sticky on scroll"},
        {"name": "Primary Button", "type": "control", "notes": "Used for CTAs"},
        {"name": "Login Form", "type": "form", "notes": "Email + Password"},
        {"name": "Card", "type": "display", "notes": "Image + title + actions"},
    ]
    issues = [
        {
            "id": "a11y-contrast",
            "severity": "medium",
            "title": "Low color contrast detected on primary button",
            "suggestion": "Increase contrast to at least 4.5:1 for normal text.",
        },
        {
            "id": "nav-focus",
            "severity": "high",
            "title": "Keyboard focus not visible on navigation links",
            "suggestion": "Add :focus styles with clear outlines.",
        },
        {
            "id": "img-alt",
            "severity": "low",
            "title": "Images missing descriptive alt text",
            "suggestion": "Provide concise alt text or mark decorative images as empty alt.",
        },
    ]

    return {
        "module": "uiux",
        "source": req.source,
        "target": req.url,
        "summary": {
            "target_host": host,
            "components_found": len(components),
            "issues_found": len(issues),
        },
        "components": components,
        "issues": issues,
    }
