# apps/server/db/base.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

raw_url = os.environ.get("DATABASE_URL")
if not raw_url:
    raise RuntimeError("DATABASE_URL is not set")

# Normalize to psycopg v3 driver
if raw_url.startswith("postgres://"):
    raw_url = raw_url.replace("postgres://", "postgresql+psycopg://", 1)
elif raw_url.startswith("postgresql://") and "+psycopg" not in raw_url and "+psycopg2" not in raw_url:
    raw_url = raw_url.replace("postgresql://", "postgresql+psycopg://", 1)

DATABASE_URL = raw_url

class Base(DeclarativeBase):
    pass

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
