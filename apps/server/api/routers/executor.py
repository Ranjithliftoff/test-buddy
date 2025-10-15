from fastapi import APIRouter
from core.base import registry
from core.models import ExecuteRequest, ExecuteResponse

router = APIRouter()

@router.post("/execute", response_model=ExecuteResponse)
def execute(req: ExecuteRequest):
    out = registry.get("executor").run(req.dict())
    return ExecuteResponse(**out)
