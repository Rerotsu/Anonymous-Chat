from fastapi import HTTPException, status


UserAlreadyExistException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь уже существует"
)

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Неверная почта или пароль"
)

CannotContainUsername = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token does not contain username",
    headers={"WWW-Authenticate": "Bearer"},
)
UserNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Пользователь не найден"
)

TokenHasExpired = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Токен не действителен"
)

IncorrectToken = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Неверный токен"
)
VerifCodeNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Верификационный код не найден или недействителен")

IncorrectVerifCode = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Неверный код"
)

IncorrectPassword = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="пароли не совпадают"
)

IncorrectFormatEmail = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Почта не действительна"
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Время токена истекло"
    )

TokenAbsentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токена не существует"
)
IncorrectTokenFormatExcpetion = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверный формат токена"
)

UserIsNotPresent = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED
)
