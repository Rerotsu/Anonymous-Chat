from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from anonymous_chat.database import get_db
from anonymous_chat.users.auth import authenticate_user, create_acces_token, get_password_hash
from anonymous_chat.users.schemas import SUserRegister, SVerifyPhone
from anonymous_chat.users.dao import UsersDAO
from anonymous_chat.Exceptions import UserAlreadyExistException, IncorrectEmailOrPasswordException

router = APIRouter(
    prefix="/user",
    tags=["Auth & Пользователи"]
)


@router.post("/auth/register")
async def register(user: SUserRegister, db: Session = Depends(get_db)):
    """
    Функция регистрации пользователя. Проверяет существует ли пользователь по почте,
    если да, возвращает ошибку UserAlreadyExistsException
    если нет, создает хеш-пароль и передает пользователя в БД

    :param user: принимает форму регистрации
    :param db: получает сессию в БД для добавления пользователя
    :retur: Сообщение "Вы успешно зарегестрировались"
    """
    existing_user = await UsersDAO.find_one_or_none(email=user.email.lower())
    if existing_user:
        raise UserAlreadyExistException
    hashed_password = get_password_hash(user.password)
    await UsersDAO.add(email=user.email, hashed_password=hashed_password)


@router.post("/auth/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_acces_token({"sub": str(user.id)})
    welcome = f'Добро пожаловать Пользователь - {user.id}'
    return {"msg": welcome, "access_token": access_token, "token_type": "bearer"}


@router.get("/confirm-email")
async def confirm_email(token: str, db: Session = Depends(get_db)):
    # Логика для подтверждения электронной почты
    pass


@router.post("/verify-phone")
async def verify_phone(phone: SVerifyPhone, db: Session = Depends(get_db)):
    # Логика для отправки кода подтверждения на номер телефона
    pass


@router.post("/confirm-phone")
async def confirm_phone(code: str, db: Session = Depends(get_db)):
    # Логика для подтверждения номера телефона
    pass
