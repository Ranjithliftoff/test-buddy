# apps/server/core/init_db.py
from db.base import engine, Base

def ensure_tables():
    print("[DB] Ensuring tables exist...")
    Base.metadata.create_all(bind=engine)
    print("[DB] Tables checked/created successfully.")
