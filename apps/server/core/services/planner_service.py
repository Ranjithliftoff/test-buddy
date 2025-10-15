from typing import Dict, Any, List
from ..base import BaseAgent

class PlannerAgent(BaseAgent):
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        intake: List[Dict[str, Any]] = payload.get("intake", [])
        bullets = [
            "Identify critical user journeys (Auth, Checkout)",
            "Design smoke scenarios for high-risk flows",
            "Draft regression coverage across modules",
        ]
        if intake:
            kinds = ", ".join(sorted({i.get("kind") for i in intake if i.get("kind")}))
            bullets.insert(0, f"Parse intake sources: {kinds}")
        return {
            "title": "High-level Test Plan",
            "bullets": bullets
        }
