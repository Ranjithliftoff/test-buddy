# apps/server/core/llm.py
from __future__ import annotations

import json
import logging
from typing import Any, Dict

from openai import OpenAI, APIConnectionError, RateLimitError, BadRequestError, AuthenticationError

from .settings import OPENAI_API_KEY, OPENAI_MODEL, LLM_TEMPERATURE

logger = logging.getLogger(__name__)


class LLM:
    """Thin wrapper around OpenAI Chat Completions that always talks to the API (no stubs)."""

    def __init__(self, model: str | None = None, temperature: float | None = None) -> None:
        if not OPENAI_API_KEY:
            # Fail fast so misconfig shows up clearly in Render logs
            raise RuntimeError("OPENAI_API_KEY is not set in the environment.")

        self.model = model or OPENAI_MODEL
        self.temperature = LLM_TEMPERATURE if temperature is None else float(temperature)
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate_json(self, system_prompt: str, user_prompt: str, *, timeout: float | None = 60.0) -> Dict[str, Any]:
        """
        Call OpenAI and return a JSON object parsed from the assistant message.
        Raises RuntimeError on any failure (network, auth, non-JSON output, etc).
        """
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                # Strongly nudge the model to return valid JSON
                response_format={"type": "json_object"},
                timeout=timeout,
            )

            content = (resp.choices[0].message.content or "").strip()
            if not content:
                raise RuntimeError("Empty response from model.")

            try:
                return json.loads(content)
            except json.JSONDecodeError as e:
                logger.exception("Failed to parse model output as JSON. Output=%r", content)
                raise RuntimeError("Model returned non-JSON output.") from e

        # Common OpenAI/HTTP exceptions get logged with stack trace, then re-raised as RuntimeError
        except (APIConnectionError, RateLimitError, BadRequestError, AuthenticationError) as e:
            logger.exception("OpenAI API error: %s", e)
            raise RuntimeError(f"OpenAI API error: {e}") from e
        except Exception as e:
            logger.exception("Unexpected error during LLM call.")
            raise RuntimeError("Unexpected error during LLM call.") from e
