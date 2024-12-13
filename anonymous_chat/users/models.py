from dataclasses import dataclass
import re
from sqlalchemy.orm import relationship

from typing import Annotated
from anyio import current_time
from fastapi import Form
from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String
from anonymous_chat.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=True, unique=True,)
    hashed_Password = Column(String, nullable=False)
    email_verified = Column(Boolean, nullable=False, default=False)
    phone_verified = Column(Boolean, nullable=False, default=False)
    email_token_verify = Column(String, nullable=True)
    phone_token_verify = Column(String, nullable=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    is_banned = Column(Boolean, nullable=False, default=False)
    created = Column(TIMESTAMP, nullable=False, default=current_time)

    message = relationship("Message", back_populates="user")
    chat_participants = relationship("ChatParticipants", back_populates="user")

    def __str__(self):
        return f"Пользователь: {self.id},{self.email},{self.phone_number}"


@dataclass
class TokenData():
    email: str


class CustomOAuth2PasswordRequestForm(BaseModel):
    email_or_number: Annotated[str, Form(...)]
    password: Annotated[str, Form(...)]

    @field_validator('email_or_number')
    def validate_username(cls, value):
        try:
            EmailStr.validate(value)
            return value
        except ValueError:
            pass
        phone_regex = r'^\+?(7|380|375)\d{9,15}$'
        if re.match(phone_regex, value):
            return value

        raise ValueError("Никнейм должен быть похож на номер телефона или Email")
