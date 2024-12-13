
from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from anonymous_chat.dao.base import BaseDAO
from anonymous_chat.chats.messages.model import Message
from anonymous_chat.database import get_db


class MessageDAO(BaseDAO):
    model = Message

    async def create_message(self, message_data: dict, db: AsyncSession = Depends(get_db)):
        message = Message(**message_data)
        db.add(message, db=db)
        await db.commit()
        await db.refresh(message)
        return message

    async def get_messages(self, chat_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(self.model).filter_by(chat_id=chat_id))
        return result.scalars().all()

    async def delete_message(self, message_id: int, db: AsyncSession = Depends(get_db)):
        stmt = delete(self.model).where(self.model.id == message_id)
        await db.execute(stmt)
        await db.commit()


"""
данная функция будет использоваться если нужен будет функционал изменения сообщения
    async def update_message(self, message_id: int, content: str, db: AsyncSession = Depends(get_db)):
        stmt = update(self.model).where(self.model.id == message_id).values(content=content)
        await db.execute(stmt)
        await db.commit()
"""
