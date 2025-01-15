import logging
from fastapi import Depends, WebSocketDisconnect
from fastapi.websockets import WebSocketState
from sqlalchemy import insert
from anonymous_chat.chats.crypto import encrypt
from anonymous_chat.chats.model import Chat
from anonymous_chat.dao.base import BaseDAO
from anonymous_chat.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from random import randint

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ChatDAO(BaseDAO):
    model = Chat

    async def create_chat_for_users(user1_id: int, user2_id: int, db: AsyncSession = Depends(get_db)) -> str:
        chat_id = randint(10000, 2147483647)
        data = {
            'id': chat_id,
            'user1_id': user1_id,
            'user2_id': user2_id,
            }
        query = insert(Chat).values(**data)
        await db.execute(query)
        await db.commit()
        return chat_id

    async def get_chat(self, chat_id, db: AsyncSession = Depends(get_db)):
        chat = await BaseDAO.find_by_id(Chat, chat_id, db=db)
        if not chat:
            return {"msg": "Чат не найден"}
        return chat

    async def handle_user(ws, other_ws, user_id, key):
        try:
            logger.info(f"Начало обработки пользователя {user_id}.")
            while True:
                if ws.client_state == WebSocketState.CONNECTED:
                    data = await ws.receive_text()
                    logger.info(f"Получено сообщение от пользователя {user_id}: {data}")
                    encrypted_message = encrypt(data, key)
                    if other_ws.client_state == WebSocketState.CONNECTED:
                        await other_ws.send_text(f"Пользователь {user_id}: {encrypted_message}")
                        logger.info(f"Сообщение отправлено пользователю {other_ws}.")
                else:
                    logger.warning(f"Соединение с пользователем {user_id} закрыто, выход из цикла.")
                    break
        except WebSocketDisconnect as e:
            logger.info(f"Пользователь {user_id} отключился. {e}")
        except Exception as e:
            logger.error(f"Ошибка при обработке пользователя {user_id}: {e}")
        finally:
            if ws.client_state == WebSocketState.CONNECTED:
                await ws.close()
                logger.info(f"Соединение с пользователем {user_id} закрыто в блоке finally.")
