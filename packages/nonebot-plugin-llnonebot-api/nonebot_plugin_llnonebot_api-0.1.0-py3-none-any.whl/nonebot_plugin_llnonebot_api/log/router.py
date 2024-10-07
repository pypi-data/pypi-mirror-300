from fastapi.websockets import WebSocketState
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ..logging import LOG_STORAGE

router = APIRouter(tags=["Log"])
active_connections: list[WebSocket] = []


@router.get("/logs", response_model=list[str])
async def system_logs_history(reverse: bool = False) -> list[str]:
    return LOG_STORAGE.list(reverse=reverse)


@router.websocket("/logs")
async def system_logs_realtime(websocket: WebSocket) -> None:
    await websocket.accept()

    async def log_listener(log: str):
        await websocket.send_text(log)

    LOG_STORAGE.listeners.add(log_listener)

    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        LOG_STORAGE.listeners.remove(log_listener)
