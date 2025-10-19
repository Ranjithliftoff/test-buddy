# apps/server/core/services/author_service.py
from __future__ import annotations
from typing import Dict, Any, List

AUTHOR_SYS = (
    "You are a Test Author. Convert scenario outlines (Given/When/Then) into:\n"
    "1) A single Gherkin feature file (.feature)\n"
    "2) A matching JavaScript step definitions file for Cypress+Cucumber.\n"
    "Keep steps reusable, use regex where possible.\n"
    'Return JSON: {"feature": {"path": string, "text": string}, "steps": {"path": string, "text": string}}\n'
)

class AuthorAgent:
    def __init__(self, name: str = "author"):
        self.name = name
        # We keep this deterministic builder for now.
        # Later you can wire the LLM like Planner/Designer if you prefer AI-authored artifacts.

    def author(self, scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Build a simple feature + steps deterministically from the given scenarios."""
        feature_lines = ["Feature: Generated Scenarios"]
        steps_lines = [
            "import { Given, When, Then } from '@badeball/cypress-cucumber-preprocessor';",
            "",
        ]

        for sc in scenarios or []:
            if not isinstance(sc, dict):
                continue

            name = sc.get("name", "Scenario")
            tags = " ".join(sc.get("tags", []))
            given = sc.get("given", [])
            when = sc.get("when", [])
            then = sc.get("then", [])

            # Build feature content
            if tags:
                feature_lines.append(tags)
            feature_lines.append(f"Scenario: {name}")
            for g in given:
                feature_lines.append(f"  Given {g}")
            for w in when:
                feature_lines.append(f"  When {w}")
            for t in then:
                feature_lines.append(f"  Then {t}")
            feature_lines.append("")

            # Build stub step definitions (can later be replaced by AI-generated ones)
            for g in given:
                steps_lines.append(f"Given('{g}', () => {{ /* TODO: implement */ }});")
            for w in when:
                steps_lines.append(f"When('{w}', () => {{ /* TODO: implement */ }});")
            for t in then:
                steps_lines.append(f"Then('{t}', () => {{ /* TODO: implement */ }});")
            steps_lines.append("")

        feature_text = "\n".join(feature_lines).strip() + "\n"
        steps_text = "\n".join(steps_lines).strip() + "\n"

        return {
            "feature": {"path": "cypress/e2e/generated.feature", "text": feature_text},
            "steps": {"path": "cypress/e2e/generated.steps.cy.js", "text": steps_text},
        }
