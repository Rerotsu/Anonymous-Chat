
import json
from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

from anonymous_chat.chats.messages.dao import MessagesDAO
from anonymous_chat.users.dao import UsersDAO
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
    messages_dao = MessagesDAO()

    while True:
        data = await websocket.receive_text()
        data = json.loads(data)

        if data['type'] == 'create_chat':
            chat_data = {
                "id": data['id']
            }
            await chats_dao.create_chat(chat_data, session)
            await websocket.send_text("Чат создан")

        elif data['type'] == 'send_message':
            message_data = {
                "chat_id": data['chat_id'],
                "user_id": data['user_id'],
                "content": data['content']
            }
            await messages_dao.create_message(message_data, session)
            await websocket.send_text("Сообщение отправлено")

        elif data['type'] == 'get_messages':
            chat_id = data['chat_id']
            messages = await messages_dao.get_messages(chat_id, session)
            await websocket.send_text(json.dumps(messages))

        elif data['type'] == 'delete_message':
            message_id = data['message_id']
            await messages_dao.delete_message(message_id, session)
            await websocket.send_text("Сообщение удалено")

        elif data['type'] == 'update_message':
            message_id = data['message_id']
            content = data['content']
            await messages_dao.update_message(message_id, content, session)
            await websocket.send_text("Сообщение обновлено")

        elif data['type'] == 'get_user_info':
            user_id = data['user_id']
            user_info = await UsersDAO.get_user_info(user_id, session)
            await websocket.send_text(json.dumps(user_info))

"""
        elif data['type'] == 'send_notification':
            notification_data = {
                "chat_id": data['chat_id'],
                "user_id": data['user_id'],
                "content": data['content']
            }
            await notifications_dao.create_notification(notification_data, session)
            await websocket.send_text("Уведомление отправлено")

        elif data['type'] == 'get_notifications':
            chat_id = data['chat_id']
            notifications = await notifications_dao.get_notifications(chat_id, session)
            await websocket.send_text(json.dumps(notifications))
"""
