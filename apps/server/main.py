from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import health, sessions, planner, designer, author, executor, curator, functional, uiux

app = FastAPI(title='Test Buddy API')

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