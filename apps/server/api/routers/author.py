from fastapi import APIRouter
from core.base import registry
from core.models import AuthorRequest, AuthorResponse

router = APIRouter()

@router.post("/author", response_model=AuthorResponse)
def author(req: AuthorRequest):
    out = registry.get("author").run(req.dict())
    return AuthorResponse(sid=req.sid, artifacts=out["artifacts"])
