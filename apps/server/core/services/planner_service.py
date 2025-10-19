# apps/server/core/services/planner_service.py
from __future__ import annotations
from typing import Dict, Any, List
from ..llm import LLM

PLANNER_SYS = (
    "You are a Test Planner. From the intake description, return concise bullets of what to test.\n"
    'Respond as JSON: {"title": string, "bullets": string[] }'
)

class PlannerAgent:
    def __init__(self, name: str = "planner"):
        self.name = name
        self.llm = LLM()

    def plan(self, intake: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Build user prompt from intake
        lines: List[str] = []
        for item in intake or []:
            kind = (item.get("kind") or "").strip()
            url = (item.get("url") or "").strip()
            note = (item.get("note") or "").strip()
            piece = " ".join(x for x in [f"- {kind}:", url, note] if x).strip()
            if piece:
                lines.append(piece)

        user = "Intake:\n" + "\n".join(lines) if lines else "Intake: (none provided)"

        # Call LLM (falls back to stub when no key)
        data = self.llm.generate_json(PLANNER_SYS, user)

        # Defensive parsing
        title = data.get("title") if isinstance(data, dict) else None
        bullets = data.get("bullets") if isinstance(data, dict) else None

        if not isinstance(title, str) or not title.strip():
            title = "Test Plan"

        if not isinstance(bullets, list):
            bullets = []
        else:
            # Normalize bullets: only strings, strip empties, dedupe, cap length
            norm = []
            seen = set()
            for b in bullets:
                if isinstance(b, str):
                    s = b.strip()
                    if s and s.lower() not in seen:
                        seen.add(s.lower())
                        norm.append(s)
            bullets = norm[:20]  # keep it tidy

        return {"title": title, "bullets": bullets}
