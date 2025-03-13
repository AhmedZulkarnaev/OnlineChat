from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict

router = APIRouter(prefix="/ws/chat")


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: Dict[int, Dict[int, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: int, user_id: int):
        """
        Устанавливает соединение с пользователем.
        websocket.accept() — подтверждает подключение.
        """
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = {}
        self.active_connections[room_id][user_id] = websocket

    def disconnect(self, room_id: int, user_id: int, username: str):
        """
        Закрывает соединение, уведомляет чат и удаляет пользователя из комнаты.
        """
        if (room_id in self.active_connections and
                user_id in self.active_connections[room_id]):
            del self.active_connections[room_id][user_id]
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def broadcast(
            self, message: str, room_id: int, sender_id: int, sender_name: str
    ):
        """
        Отправляет сообщение всем в комнате.
        """
        if room_id in self.active_connections:
            for user_id, connection in self.active_connections[room_id].items(

            ):
                message_data = {
                    "username": sender_name,
                    "text": message,
                    "is_self": user_id == sender_id
                }
                await connection.send_json(message_data)


manager = ConnectionManager()


@router.websocket("/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, user_id: int, username: str):
    await manager.connect(websocket, room_id, user_id)
    await manager.broadcast(f"{username} присоединился к чату", room_id, user_id, "Сервер")

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data, room_id, user_id, username)
    except WebSocketDisconnect:
        manager.disconnect(room_id, user_id, username)
        await manager.broadcast(f"{username} покинул чат.", room_id, user_id, "Сервер")
