
import json
from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

from anonymous_chat.chats.messages.dao import MessageDAO
from anonymous_chat.users.dao import UserDAO
from anonymous_chat.chats.dao import ChatDAO
from anonymous_chat.database import get_db


router = APIRouter(
    prefix="/chat",
    tags=["Чат"]
)


@router.websocket("/ce")
async def chat_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db)):
    await websocket.accept()
    chats_dao = ChatDAO()
    messages_dao = MessageDAO()

    while True:
        data = await websocket.receive_text()
        data = json.loads(data)

        if data['type'] == 'find_chat':
            chat_data = {
                "id": data['id']
            }
            await chats_dao.create_chat(chat_data, db)
            await websocket.send_text("Чат создан")

        elif data['type'] == 'send_message':
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

        elif data['type'] == 'get_user_info':
            user_id = data['user_id']
            user_info = await UserDAO.get_user_info(user_id, db)
            await websocket.send_text(json.dumps(user_info))
"""
        elif data['type'] == 'delete_message':
            message_id = data['message_id']
            await messages_dao.delete_message(message_id, db)
            await websocket.send_text("Сообщение удалено")

        elif data['type'] == 'send_notification':
            notification_data = {
                "chat_id": data['chat_id'],
                "user_id": data['user_id'],
                "content": data['content']
            }
            await notifications_dao.create_notification(notification_data, db)
            await websocket.send_text("Уведомление отправлено")

        elif data['type'] == 'get_notifications':
            chat_id = data['chat_id']
            notifications = await notifications_dao.get_notifications(chat_id, db)
            await websocket.send_text(json.dumps(notifications))
"""
