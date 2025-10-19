# apps/server/main.py
from __future__ import annotations

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Fail fast if DB driver is missing/mismatched
from core import db_check
db_check.check_db_driver()

# Agents (keep these if your routes depend on them)
from core.base import registry
from core.services.planner_service import PlannerAgent
from core.services.designer_service import DesignerAgent
from core.services.author_service import AuthorAgent
from core.services.executor_service import ExecutorAgent
from core.services.curator_service import CuratorAgent

# Routers
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

API_PREFIX = "/api"

app = FastAPI(title="Test Buddy API", version="4.0")

# CORS – tighten to your frontend origin when ready
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # e.g., ["https://your-frontend.domain"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register agents (if used by routes)
registry.register(PlannerAgent("planner"))
registry.register(DesignerAgent("designer"))
registry.register(AuthorAgent("author"))
registry.register(ExecutorAgent("executor"))
registry.register(CuratorAgent("curator"))

# Public health route
app.include_router(health.router)  # /health

# Feature routes under /api/*
app.include_router(sessions.router,   prefix=API_PREFIX)
app.include_router(planner.router,    prefix=API_PREFIX)
app.include_router(designer.router,   prefix=API_PREFIX)
app.include_router(author.router,     prefix=API_PREFIX)
app.include_router(executor.router,   prefix=API_PREFIX)
app.include_router(curator.router,    prefix=API_PREFIX)
app.include_router(functional.router, prefix=API_PREFIX)
app.include_router(uiux.router,       prefix=API_PREFIX)

@app.get("/")
def root():
    return {
        "ok": True,
        "service": "test-buddy-api",
        "docs": "/docs",
        "health": "/health",
        "api_base": API_PREFIX,
    }
