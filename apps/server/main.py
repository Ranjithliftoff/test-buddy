# apps/server/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.base import registry
from core.services.planner_service import PlannerAgent
from core.services.designer_service import DesignerAgent
from core.services.author_service import AuthorAgent
from core.services.executor_service import ExecutorAgent
from core.services.curator_service import CuratorAgent

# Fail fast in deploy logs if no PostgreSQL driver is present
from core import db_check
from core.init_db import ensure_tables

db_check.check_db_driver()

# Import routers only after the driver check so the error shows up clearly
from api.routers import (
    health,
    sessions,
    planner,
    designer,
    author,
    executor,
    curator,
    functional,
    uiux,
)


app = FastAPI(title="Test Buddy API")

# Register agents
registry.register(PlannerAgent("planner"))
registry.register(DesignerAgent("designer"))
registry.register(AuthorAgent("author"))
registry.register(ExecutorAgent("executor"))
registry.register(CuratorAgent("curator"))

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router)
app.include_router(sessions.router)
app.include_router(planner.router)
app.include_router(designer.router)
app.include_router(author.router)
app.include_router(executor.router)
app.include_router(curator.router)
app.include_router(functional.router)
app.include_router(uiux.router)

# Create tables if they don't exist (safe to run every boot)
@app.get("/")
def root():
    return {"ok": True, "service": "test-buddy-api", "docs": "/docs", "health": "/health"}

# ✅ ADD THIS
@app.on_event("startup")
def _startup_create_tables():
    """Ensure database tables exist on startup."""
    ensure_tables()