from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from anonymous_chat.database import Base


class ChatParticipants(Base):
    __tablename__ = "chat_participants"

    chat_id = Column(Integer, ForeignKey('chats.id'), primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    chat = relationship("Chat", back_populates="chat_participants")
    user = relationship("User", back_populates="chat_participants")


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)

    messages = relationship("Message", back_populates="chat")
    chat_participants = relationship("ChatParticipants", back_populates="chat")
