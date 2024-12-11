from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from anonymous_chat.database import Base


class chat_participants(Base):
    __tablename__ = "chat_participants"

    chat_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    chats = relationship("Chat", back_populates="chat_participants")


class Chats(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)

    messages = relationship("Message", back_populates="chat")
    participants = relationship("User", back_populates="chats")
