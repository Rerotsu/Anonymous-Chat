
from fastapi import Depends
from anonymous_chat.dao.base import BaseDAO
from anonymous_chat.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession


class ChatsDao(BaseDAO):
    model = Chats

    async def create_chat(self, chat_data: dict, db: AsyncSession = Depends(get_db)):
        new_chat = Chats(**chat_data)  # Предполагая, что Chats - это ваша модель
        db.add(new_chat)
        await db.commit()  # Асинхронное сохранение
        return new_chat

    def get_chat(self, chat_id):
        # Логика для получения чата по ID
        pass

    def get_all_chats(self):
        # Логика для получения всех чатов
        pass