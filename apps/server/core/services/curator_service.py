from typing import Dict, Any
from ..base import BaseAgent

class CuratorAgent(BaseAgent):
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        insights = [
            {"id": "ins-1", "kind": "flaky", "text": "Login intermittently fails on CI"},
            {"id": "ins-2", "kind": "regression", "text": "Auth latency increased in latest build"},
        ]
        return {"insights": insights}
