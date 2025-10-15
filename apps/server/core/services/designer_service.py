from typing import Dict, Any, List
from ..base import BaseAgent

class DesignerAgent(BaseAgent):
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        plan_ids: List[str] = payload.get("plan_ids", [])
        scenarios = [{
            "id": "scn-1",
            "name": "Login works" + (f" (from {plan_ids[0]})" if plan_ids else ""),
            "given": ["user at /login"],
            "when": ["user submits valid credentials"],
            "then": ["redirect to dashboard"]
        }]
        return {"scenarios": scenarios}
