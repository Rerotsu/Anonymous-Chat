from datetime import datetime, timedelta, timezone
import random
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from twilio.rest import Client

from jose import jwt
from passlib.context import CryptContext
import smtplib

from anonymous_chat.config import settings
from anonymous_chat.database import get_db
from anonymous_chat.users.dao import UserDAO
from anonymous_chat.users.models import TokenData, User
from anonymous_chat.Exceptions import CannotContainUsername


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def create_acces_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=2)
    to_encode.update({"exp": expire, "sub": data.get("email")})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt


async def create_email_confirmation_token(email: str):
    expiration = datetime.now(timezone.utc) + timedelta(hours=1)
    payload = {"sub": email, "exp": expiration}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


async def send_confirmation_email(email, token):
    confirmation_url = f"http://yourdomain.com/confirm-email?token={token}"
    try:
        smtpObj = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        smtpObj.starttls()
        smtpObj.login(settings.SMTP_USER, settings.SMTP_PASS)

        message = f"Подтвердите Электронную почту, для доступа к функциям сайта {confirmation_url}"
        smtpObj.sendmail(settings.SMTP_USER, email, message)
        smtpObj.quit()
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")


async def generate_verification_code() -> str:
    return str(random.randint(100000, 999999))


async def send_sms(phone: str, code: str):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body=f'Код подтверждения для Anon.chat: {code}',
            from_=settings.NUMBER,
            to=phone
        )
        return message
    except Exception as e:
        raise e


async def get_stored_code(phone_number, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone_number == phone_number).first()
    if user:
        return user.phone_token_verify
    else:
        return None


async def verify_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: Optional[str] = payload.get("sub")

        if email is None:
            raise CannotContainUsername
        return TokenData(username=email)
    except Exception as e:
        raise e


async def authenticate_user(identifier: str, password: str, db: AsyncSession = Depends(get_db)):
    # Сначала проверяем по email
    user = await UserDAO.find_one_or_none(db=db, email=identifier)
    if not user or not await verify_password(password, user.hashed_password):
        return None
    return user
