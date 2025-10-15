from fastapi import APIRouter

router = APIRouter(prefix="/plan", tags=["planner"])


@router.get("/")
async def plan_root():
    return {"message": "planner root"}
