import logging
import asyncio
from collections import deque
from fastapi import APIRouter, Depends, Query, WebSocket
from fastapi.websockets import WebSocketState
from anonymous_chat.chats.crypto import generate_key
from anonymous_chat.chats.dao import ChatDAO
from anonymous_chat.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="",
    tags=["Чат"]
)

waiting_users = deque()
active_connections = {}


@router.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket, user_id: int = Query(...), db: AsyncSession = Depends(get_db)):

    logger.info(f"Пользователь {user_id} подключился.")
    await websocket.accept()
    key = generate_key()
    waiting_users.append(websocket)
    active_connections[websocket] = user_id

    if len(waiting_users) >= 2:
        user1_ws = waiting_users.popleft()
        user2_ws = waiting_users.popleft()
        user1_id = active_connections[user1_ws]
        user2_id = active_connections[user2_ws]

        logger.info(f"Создание чата для пользователей {user1_id} и {user2_id}.")
        try:
            chat_id = await ChatDAO.create_chat_for_users(user1_id, user2_id, db)
            logger.info(f"Чат создан с ID {chat_id}. Уведомление пользователей.")
            if user1_ws.client_state == WebSocketState.CONNECTED:
                if user2_ws.client_state == WebSocketState.CONNECTED:
                    await asyncio.gather(
                        await ChatDAO.handle_user(user1_ws, user2_ws, user1_id, key),
                        await ChatDAO.handle_user(user2_ws, user1_ws, user2_id, key)
                    )
        except Exception as e:
            logger.error(f"Ошибка при создании чата: {e}")
        finally:
            if user1_ws.client_state == WebSocketState.CONNECTED:
                await user1_ws.close()
                logger.info(f"Соединение с пользователем {user1_id} закрыто.")
            if user2_ws.client_state == WebSocketState.CONNECTED:
                await user2_ws.close()
                logger.info(f"Соединение с пользователем {user2_id} закрыто.")
