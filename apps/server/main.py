from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.base import registry
from core.services.planner_service import PlannerAgent
from core.services.designer_service import DesignerAgent
from core.services.author_service import AuthorAgent
from core.services.executor_service import ExecutorAgent
from core.services.curator_service import CuratorAgent

from api.routers import health, sessions, planner, designer, author, executor, curator, functional, uiux

app = FastAPI(title='Test Buddy API')

registry.register(PlannerAgent("planner"))
registry.register(DesignerAgent("designer"))
registry.register(AuthorAgent("author"))
registry.register(ExecutorAgent("executor"))
registry.register(CuratorAgent("curator"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(sessions.router)
app.include_router(planner.router)
app.include_router(designer.router)
app.include_router(author.router)
app.include_router(executor.router)
app.include_router(curator.router)
app.include_router(functional.router)
app.include_router(uiux.router)