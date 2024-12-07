from datetime import datetime, timedelta, timezone
from typing import Optional

from jose.jwt import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from anonymous_chat.config import settings
from anonymous_chat.users.dao import UsersDAO
from anonymous_chat.users.models import TokenData
from anonymous_chat.Exceptions import CannotContainUsername


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_acces_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=120)
    to_encode.update({"exp": expire, "sub": data.get("email")})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt


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
