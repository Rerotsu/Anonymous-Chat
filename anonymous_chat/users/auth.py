from datetime import datetime, timedelta, timezone
from typing import Optional

from jose.jwt import jwt
from passlib.context import CryptContext
from pydantic import EmailStr
import smtplib

from anonymous_chat.config import settings
from anonymous_chat.users.dao import UsersDAO
from anonymous_chat.users.models import TokenData
from anonymous_chat.Exceptions import CannotContainUsername


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

smtpObj = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
smtpObj.starttls()
smtpObj.login(settings.SMTP_USER, settings.SMTP_PASS)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_acces_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=2)
    to_encode.update({"exp": expire, "sub": data.get("email")})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt


def create_email_confirmation_token(email: str):
    expiration = datetime.now(timezone.utc) + timedelta(hours=1)
    payload = {"sub": email, "exp": expiration}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


async def verify_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: Optional[str] = payload.get("sub")

        if email is None:
            raise CannotContainUsername
        return TokenData(username=email)
    except Exception as e:
        raise e


async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
