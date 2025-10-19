# apps/server/api/routers/health.py
from fastapi import APIRouter
from db.base import SessionLocal
import os

router = APIRouter(tags=["health"])

@router.get("/health")
def health():
    """Basic API health check endpoint."""
    return {"ok": True, "service": "TestBuddy API", "docs": "/docs"}

@router.get("/health/openai")
def check_openai_key():
    """Checks whether the OpenAI API key is loaded properly."""
    key = os.getenv("OPENAI_API_KEY", None)
    if key and key.startswith("sk-"):
        return {"openai_key_loaded": True, "prefix": key[:7] + "..."}
    else:
        return {"openai_key_loaded": False, "message": "Key not found or invalid"}

@router.get("/health/db")
def health_db():
    db = SessionLocal()
    try:
        v = db.execute(text("select version()")).scalar()
        return {"ok": True, "version": v}
    finally:
        db.close()