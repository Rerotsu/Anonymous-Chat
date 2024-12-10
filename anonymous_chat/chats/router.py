
from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

from anonymous_chat.chats.crypto import encrypt, generate_key
from anonymous_chat.chats.dao import ChatsDao
from anonymous_chat.database import async_session_maker


router = APIRouter(
    prefix="/chat",
    tags=["Чат"]
)

chats_dao = ChatsDao()


@router.websocket("/ws")
async def chat_endpoint(websocket: WebSocket, session: AsyncSession = Depends(async_session_maker)):
    await websocket.accept()
    chats_dao = ChatsDao()

    while True:
        data = await websocket.receive_text()

        key = generate_key()
        encrypted_message = encrypt(data, key)

        chat_data = {
            "message": encrypted_message,
            # Добавьте другие поля, если необходимо, например, user_id, timestamp и т.д.
        }

        await chats_dao.create_chat(chat_data, session)

        await websocket.send_text(f"Сообщение сохранено: {data}")
