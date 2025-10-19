import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # pick your default
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.2"))
