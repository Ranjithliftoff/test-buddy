from fastapi import APIRouter

import os


router = APIRouter()

@router.get("/health")
def health():
    return {"ok": True, "service": "TestBuddy API"}


@router.get("/health/openai")
def check_openai_key():
    key = os.getenv("OPENAI_API_KEY", None)
    if key and key.startswith("sk-"):
        return {"openai_key_loaded": True, "prefix": key[:7] + "..."}
    else:
        return {"openai_key_loaded": False, "message": "Key not found or invalid"}
