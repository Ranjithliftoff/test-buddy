# apps/server/api/routers/debug_db.py
from fastapi import APIRouter
from sqlalchemy import text
from db.base import engine, SessionLocal
import uuid

router = APIRouter(tags=["_debug"])

@router.get("/_debug/db-ping")
def db_ping():
    try:
        with engine.connect() as conn:
            conn.execute(text("select 1"))
        return {"ok": True, "message": "DB connection OK"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@router.post("/_debug/db-insert-session")
def db_insert_session():
    from db import models as m  # lazy import so it doesn’t run at import time
    try:
        db = SessionLocal()
        s = m.Session(module="functional")  # minimal required field
        db.add(s)
        db.commit()
        db.refresh(s)
        return {"ok": True, "session_id": str(s.id)}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        try:
            db.close()
        except:  # noqa
            pass
