from fastapi import HTTPException, status


UserAlreadyExistException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь уже существует"
)

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверная почта или пароль"
)

CannotContainUsername = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token does not contain username",
    headers={"WWW-Authenticate": "Bearer"},
)
