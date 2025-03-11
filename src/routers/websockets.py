from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.models.blog import Blog as BlogModel

router = APIRouter()

active_connections: List[WebSocket] = []


@router.websocket("/ws/blogs")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)


async def broadcast_new_blog(blog_data: BlogModel):
    message = {
        "event": "new_blog",
        "title": blog_data.title,
        "author": blog_data.written_by.username,
    }

    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except:
            disconnected.append(connection)

    for conn in disconnected:
        active_connections.remove(conn)
