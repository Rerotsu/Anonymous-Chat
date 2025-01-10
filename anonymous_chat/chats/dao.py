from fastapi import Depends
from sqlalchemy import insert
from anonymous_chat.chats.model import Chat
from anonymous_chat.dao.base import BaseDAO
from anonymous_chat.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from random import randint


class ChatDAO(BaseDAO):
    model = Chat

    async def create_chat_for_users(user1_id: int, user2_id: int, db: AsyncSession = Depends(get_db)) -> str:
        chat_id = randint(10000, 9999999999)
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
