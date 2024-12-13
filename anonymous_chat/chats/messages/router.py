

import json
from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

from anonymous_chat.chats.messages.dao import MessageDAO
from anonymous_chat.database import get_db


router = APIRouter(
    prefix="/messages",
    tags=["Сообщения"]
)


@router.websocket("/cm")
async def create_messages_in_chat(websocket: WebSocket, message_data: dict, db: AsyncSession = Depends(get_db)):
    await websocket.accept()
    messages_dao = MessageDAO()

    while True:
        data = await websocket.receive_text()
        data = json.loads(data)

        if data['type'] == 'send_message':
            message_data = {
                "chat_id": data['chat_id'],
                "user_id": data['user_id'],
                "content": data['content']
            }
            await messages_dao.create_message(message_data, db)
            await websocket.send_text("Сообщение отправлено")

        elif data['type'] == 'get_messages':
            chat_id = data['chat_id']
            messages = await messages_dao.get_messages(chat_id, db)
            await websocket.send_text(json.dumps(messages))

        elif data['type'] == 'delete_message':
            message_id = data['message_id']
            await messages_dao.delete_message(message_id, db)
            await websocket.send_text("Сообщение удалено")
