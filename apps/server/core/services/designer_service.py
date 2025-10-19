# apps/server/core/services/designer_service.py
from __future__ import annotations
from typing import Dict, Any, List
from ..llm import LLM

DESIGNER_SYS = (
    "You are a Test Designer. Convert the plan bullets into scenario outlines.\n"
    'Respond as JSON: {"scenarios": ['
    '{"name": string, "tags": string[], "given": string[], "when": string[], "then": string[]}'
    ']}'
)

class DesignerAgent:
    def __init__(self, name: str = "designer"):
        self.name = name
        self.llm = LLM()

    def design(self, plan_bullets: List[str], seed_outline: str | None = None) -> Dict[str, Any]:
        # Build prompt
        bullet_lines = [f"- {b}" for b in (plan_bullets or []) if isinstance(b, str) and b.strip()]
        user = "Plan bullets:\n" + "\n".join(bullet_lines) if bullet_lines else "Plan bullets: (none provided)"
        if seed_outline:
            user += f"\n\nSeed outline:\n{seed_outline.strip()}"

        # Query LLM
        data = self.llm.generate_json(DESIGNER_SYS, user)

        # Safe normalization
        scenarios = data.get("scenarios") if isinstance(data, dict) else None
        if not isinstance(scenarios, list):
            scenarios = []

        clean_scenarios = []
        for s in scenarios:
            if not isinstance(s, dict):
                continue
            clean_scenarios.append({
                "name": s.get("name", "Unnamed Scenario"),
                "tags": s.get("tags", []),
                "given": s.get("given", []),
                "when": s.get("when", []),
                "then": s.get("then", []),
            })

        return {"scenarios": clean_scenarios}
