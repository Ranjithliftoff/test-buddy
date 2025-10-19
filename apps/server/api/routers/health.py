# apps/server/api/routers/health.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text
from db.base import SessionLocal, DATABASE_URL
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
        row = db.execute(text("select current_database(), version()")).fetchone()
        return {
            "ok": True,
            "dsn_host": DATABASE_URL.split('@')[-1].split('?')[0],  # just to confirm host/port
            "database": row[0],
            "version": row[1][:80],
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"ok": False, "error": str(e), "type": e.__class__.__name__},
        )
    finally:
        try:
            db.close()
        except:
            pass