from typing import Dict, Any
from ..base import BaseAgent

class PlannerAgent(BaseAgent):
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        goals = payload.get("goals", [])
        items = [
            {"id": "plan-1", "title": "Auth flow", "rationale": "High impact"},
            {"id": "plan-2", "title": "Checkout smoke", "rationale": "Critical path"},
        ]
        if goals:
            items.append({"id": "plan-3", "title": goals[0], "rationale": "User goal"})
        return {"items": items}
