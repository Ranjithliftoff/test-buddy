from typing import Dict, Any, List
from ..base import BaseAgent

FEATURE_TMPL = """Feature: {title}

  Scenario: {scn1}
    Given I am on the login page
    When I submit valid credentials
    Then I should land on the dashboard

  Scenario: {scn2}
    Given I am on the login page
    When I submit invalid credentials
    Then I should see an error message
"""

STEP_TMPL = """import {{ Given, When, Then }} from "@badeball/cypress-cucumber-preprocessor";

Given("I am on the login page", () => {{
  cy.visit("/login");
}});

When("I submit valid credentials", () => {{
  cy.get('[name="email"]').type("user@example.com");
  cy.get('[name="password"]').type("correct-horse-battery-staple");
  cy.contains("button","Sign in").click();
}});

When("I submit invalid credentials", () => {{
  cy.get('[name="email"]').type("user@example.com");
  cy.get('[name="password"]').type("wrong");
  cy.contains("button","Sign in").click();
}});

Then("I should land on the dashboard", () => {{
  cy.url().should("include", "/dashboard");
}});

Then("I should see an error message", () => {{
  cy.contains(/invalid|error/i).should("be.visible");
}});
"""

class AuthorAgent(BaseAgent):
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        scenarios: List[str] = payload.get("scenarios") or [
            "Login works with valid credentials",
            "Login prevents access with invalid credentials"
        ]
        title = "Authentication"

        feature_text = FEATURE_TMPL.format(
            title=title,
            scn1=scenarios[0],
            scn2=scenarios[1] if len(scenarios) > 1 else "Login prevents access with invalid credentials"
        )
        step_text = STEP_TMPL

        artifacts = [{
            "id": "auth-login",
            "toolchain": "cypress-cucumber",
            "feature_path": "cypress/e2e/auth/login.feature",
            "feature_text": feature_text,
            "step_path": "cypress/e2e/auth/login.steps.js",
            "step_text": step_text
        }]
        return {
            "summary": f"Generated {len(artifacts)} Cypress+Cucumber artifact(s)",
            "artifacts": artifacts
        }
