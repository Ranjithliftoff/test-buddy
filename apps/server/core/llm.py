from __future__ import annotations
import json
from typing import Any, Dict
from openai import OpenAI
from .settings import OPENAI_API_KEY, OPENAI_MODEL, LLM_TEMPERATURE


class LLM:
    """Minimal wrapper. Uses OpenAI API if key present, otherwise returns safe stub JSON."""

    def __init__(self, model: str | None = None, temperature: float | None = None):
        self.model = model or OPENAI_MODEL
        self.temperature = LLM_TEMPERATURE if temperature is None else temperature
        self.client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

    def generate_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        if not self.client:
            # ---- Safe stub for local/dev/no-key ----
            sp = system_prompt.lower()
            if "test designer" in sp or "designer" in sp:
                return {
                    "scenarios": [
                        {
                            "name": "Login works with valid credentials",
                            "tags": ["@smoke"],
                            "given": ["I am on the login page"],
                            "when": ["I log in with username 'user' and password 'pass'"],
                            "then": ["I should see the dashboard"]
                        }
                    ]
                }
            if "test planner" in sp or "planner" in sp:
                return {"title": "Functional Plan", "bullets": ["Cover login", "Cover logout"]}
            return {}

        # ---- Real API call ----
        resp = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        text = resp.choices[0].message.content.strip()
        try:
            return json.loads(text)
        except Exception:
            # If model output isn't valid JSON, fallback safely
            return {"raw_response": text}
