from datetime import datetime, timezone

from fastapi import Depends, Request
from jose import JWTError, jwt
from anonymous_chat.users.dao import UserDAO
from anonymous_chat.config import settings
from anonymous_chat.Exceptions import (
    TokenAbsentException,
    IncorrectTokenFormatExcpetion,
    TokenExpiredException,
    UserIsNotPresent
)


def get_token(request: Request):
    token = request.cookies.get("anon_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise IncorrectTokenFormatExcpetion

    expire: str = payload.get("exp")
    if (not expire) or (int(expire < datetime.now(timezone.utc).timestamp())):
        raise TokenExpiredException

    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresent

    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresent
