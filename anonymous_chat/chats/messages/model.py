
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from anonymous_chat.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey('chats.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, server_default=func.now())

    chat = relationship("Chat", back_populates="message")
    user = relationship("User", back_populates="message")