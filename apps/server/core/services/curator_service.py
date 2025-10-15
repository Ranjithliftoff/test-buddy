from typing import Dict, Any, List
from ..base import BaseAgent

class CuratorAgent(BaseAgent):
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        run_id = payload.get("run_id", "run-001")
        insights: List[Dict[str, Any]] = [
            {"id": "ins-1", "kind": "flaky", "text": "Login error toast flaps on slow network"},
            {"id": "ins-2", "kind": "regression", "text": "Auth response time increased by 30%"},
        ]
        return {"run_id": run_id, "insights": insights}
