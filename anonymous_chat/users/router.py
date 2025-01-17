from datetime import datetime
import re

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt

from anonymous_chat.database import get_db
from anonymous_chat.users.auth import (
    authenticate_user,
    create_acces_token,
    create_email_confirmation_token,
    generate_verification_code,
    get_password_hash,
    get_stored_code,
    send_confirmation_email,
    send_sms,
)
from anonymous_chat.users.dependencies import get_current_user
from anonymous_chat.users.models import CustomOAuth2PasswordRequestForm, User
from anonymous_chat.users.schemas import SUserRegister, SVerifyPhone
from anonymous_chat.users.dao import UserDAO
from anonymous_chat.config import settings
from anonymous_chat.Exceptions import (
    IncorrectFormatEmail,
    IncorrectEmailOrPasswordException,
    IncorrectPassword,
    IncorrectToken,
    TokenHasExpired,
    UserAlreadyExistException,
    UserNotFound,
    VerifCodeNotFound,
)
import logging


router = APIRouter(
    prefix="",
    tags=["Auth & Пользователи"]
)

logger = logging.getLogger(__name__)


@router.post("/auth/register")
async def register(user: SUserRegister, db: AsyncSession = Depends(get_db)):
    """
    Функция регистрации пользователя. Проверяет существует ли пользователь по почте,
    если да, возвращает ошибку UserAlreadyExistsException
    если нет, создает хеш-пароль и передает пользователя в БД

    :param user: принимает форму регистрации
    :param db: получает сессию в БД для добавления пользователя
    :retur: Сообщение "Вы успешно зарегестрировались"
    """
    if not re.match(
        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", user.email
    ):
        raise IncorrectFormatEmail
    """
    надо добавить проверку на номер телефона

    """
    existing_user = await UserDAO.find_one_or_none(db=db, email=user.email.lower())
    if existing_user:
        raise UserAlreadyExistException

    if user.password != user.confirm_password:
        raise IncorrectPassword

    hashed_password = await get_password_hash(user.password)
    email_token = await create_email_confirmation_token(user.email)
    await send_confirmation_email(user.email, email_token)

    await UserDAO.add(
        db=db,
        email=user.email,
        phone_number=user.phone_number,
        hashed_password=hashed_password,
        email_token_verify=email_token,
        created=datetime.now(),
    )

    welcome = "Вы успешно зарегестрировались, Пожалуйста, подтвердите Электронную почту, чтобы открыть большенство функций сайта"
    return {"msg": welcome}


@router.post("/auth/login")
async def login_user(
    response: Response,
    form_data: CustomOAuth2PasswordRequestForm,
    db: AsyncSession = Depends(get_db),
):
    """
    Функция Логина пользователя. Проверяет действительна ли функция и существует ли пользователь
    если нет, возвращает ошибку IncorrecrtLoginOrPasswordExcaption
    если да, создает токен в куках для входа

    :param form_data: кастомная форма входа
    :param db: сессия ДБ
    :return: Сообщение о успешном входе, токен и формат токена
    """
    if not re.match(
        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", form_data.email
    ):
        raise IncorrectFormatEmail

    user = await authenticate_user(form_data.email, form_data.password, db)

    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = await create_acces_token({"sub": str(user.id)})
    response.set_cookie("anon_access_token", access_token, httponly=True,)
    return access_token


@router.post("/user/logout")
async def logout_user(response: Response):
    response.delete_cookie("anon_access_token")


@router.get("/user/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/confirm-email")
async def confirm_email(token: str, db: AsyncSession = Depends(get_db)):
    """
    Функция подтверждения Email'а. Создается токен и отправляется письмом на почту

    :param token: Пользователь переходит по ссылке с токеном
    :param db: получение сессии БД
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email = payload.get("sub")

        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise UserNotFound

        user.email_verified = True
        db.commit()

        return {"msg": "Почта подтвержена, спасибо"}
    except jwt.ExpiredSignatureError:
        raise TokenHasExpired
    except jwt.JWTError:
        raise IncorrectToken


@router.post("/send_verify-phone")
async def send_verify_phone(
    phone_schemas: SVerifyPhone, db: AsyncSession = Depends(get_db)
):
    """
    Функция для отправки верифицкационного кода на номер телефона пользователя.

    :param phone_shcemas: форма для ввода номера телефона
    :param db: получение сессии БД
    """
    user = db.query(User).filter(User.phone == phone_schemas.phone_number).first()
    if not user:
        raise UserNotFound

    code = generate_verification_code()
    await send_sms(phone_schemas.phone_number, code)

    user.phone_token_verify = code
    db.commit()

    return {"msg": "Код отправлен"}


@router.post("/verify-phone")
async def verify_phone(phone_schemas: SVerifyPhone, db: AsyncSession = Depends(get_db)):
    """
    Функция для верификации номера телефона

    :param phone: форма для ввода номера телефона
    :param db: получение сессии БД
    """
    user = db.query(User).filter(User.phone == phone_schemas.phone).first()
    if not user:
        raise UserNotFound

    stored_code = get_stored_code(phone_schemas.phone)
    if stored_code is None:
        raise VerifCodeNotFound

    if stored_code != phone_schemas.code:
        raise VerifCodeNotFound

    user.phone_verified = True
    db.commit()

    return {"msg": "Номер телефона подтвержден"}
