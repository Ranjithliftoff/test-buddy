# apps/server/core/init_db.py
from db.base import Base, engine

def ensure_tables() -> None:
    # Simple bootstrap: create tables if they don't exist.
    # You can switch to Alembic later for real migrations.
    Base.metadata.create_all(bind=engine)
