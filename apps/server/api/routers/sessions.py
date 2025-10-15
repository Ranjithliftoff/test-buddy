from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/sessions", tags=["sessions"])


class SessionCreate(BaseModel):
    name: str


@router.post("/create")
async def create_session(payload: SessionCreate):
    return {"session_id": "sess_123", "name": payload.name}
