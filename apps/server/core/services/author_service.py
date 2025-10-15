from typing import Dict, Any, List
from ..base import BaseAgent

class AuthorAgent(BaseAgent):
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        scenario_ids: List[str] = payload.get("scenario_ids", [])
        artifacts = [{
            "id": "art-1",
            "framework": "playwright",
            "code": "test('login', async ({ page }) => { /* ... */ })" + (f" // {scenario_ids[0]}" if scenario_ids else "")
        }]
        return {"artifacts": artifacts}
