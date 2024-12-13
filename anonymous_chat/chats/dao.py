from fastapi import Depends
from anonymous_chat.chats.model import Chat
from anonymous_chat.dao.base import BaseDAO
from anonymous_chat.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession


class ChatDAO(BaseDAO):
    model = Chat

    async def create_chat(self, chat_data: dict, db: AsyncSession = Depends(get_db)):
        new_chat = Chat(**chat_data)
        db.add(new_chat)
        await db.commit()
        return new_chat

    async def get_chat(self, chat_id, db: AsyncSession = Depends(get_db)):
        chat = await BaseDAO.find_by_id(Chat, chat_id, db=db)
        if not chat:
            return {"msg": "Чат не найден"}
        return chat
