from typing import Dict, Any, List
from ..base import BaseAgent

class DesignerAgent(BaseAgent):
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        outline: str = payload.get("outline") or "Auth + Smoke baseline"
        scenarios: List[str] = [
            "Login works with valid credentials",
            "Login prevents access with invalid credentials",
            "User can logout from dashboard"
        ]
        if "checkout" in outline.lower():
            scenarios.append("Checkout completes with valid card")
        return {
            "title": f"Scenarios from outline: {outline}",
            "scenarios": scenarios
        }
