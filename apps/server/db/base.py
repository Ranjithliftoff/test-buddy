import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

class Base(DeclarativeBase):
    pass

# Normalize common Heroku/Render-style URL prefixes and prefer psycopg (psycopg3)
# so SQLAlchemy will use the psycopg DBAPI instead of psycopg2 which can fail
# on some modern Python builds when an incompatible binary wheel is present.
if DATABASE_URL.startswith("postgres://"):
    # Convert the deprecated short scheme to full scheme
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# If the URL does not specify a DBAPI, prefer psycopg (psycopg3)
if DATABASE_URL.startswith("postgresql://") and "+psycopg" not in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

# If someone provided a URL that explicitly used psycopg2, prefer psycopg (psycopg3)
# to avoid loading the legacy psycopg2 binary which can be incompatible with
# newer Python builds on some hosting platforms.
if "+psycopg2" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("+psycopg2", "+psycopg")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
