from datetime import datetime, timezone

from fastapi import Depends, Request
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from anonymous_chat.database import get_db
from anonymous_chat.users.dao import UserDAO
from anonymous_chat.config import settings
from anonymous_chat.Exceptions import (
    TokenAbsentException,
    IncorrectTokenFormatException,
    TokenExpiredException,
    UserIsNotPresent
)


def get_token(request: Request) -> str:
    token = request.cookies.get("anon_access_token")
    if not token:
        raise TokenAbsentException
    return str(token)


async def get_current_user(token: str = Depends(get_token), db: AsyncSession = Depends(get_db)):
    print(f"Received token: {token}")

    if not isinstance(token, str) or len(token.split('.')) != 3:
        print("причина в .")
        raise IncorrectTokenFormatException

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError as e:
        print(f"дошло до трай {e}")
        raise IncorrectTokenFormatException

    expire: str = payload.get("exp")
    if not expire or int(expire) < datetime.now(timezone.utc).timestamp():
        raise TokenExpiredException

    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresent

    user = await UserDAO.find_by_id(int(user_id), db=db)
    if not user:
        raise UserIsNotPresent
    
    return user
