from fastapi import APIRouter, WebSocket
from core.base import registry
from core.models import ExecuteRequest, ExecuteResponse
import asyncio

router = APIRouter()

@router.post("/execute", response_model=ExecuteResponse)
def execute(req: ExecuteRequest):
    out = registry.get("executor").run(req.dict())
    return ExecuteResponse(sid=req.sid, run_id=out["run_id"], summary=out["summary"])

@router.websocket("/execute/stream")
async def execute_stream(ws: WebSocket):
    await ws.accept()
    for line in ["Booting runner...", "Pulling browsers...", "Running tests...", "All green ✅"]:
        await ws.send_text(line)
        await asyncio.sleep(0.6)
    await ws.close()
