from pydantic import BaseModel, EmailStr


class SUserRegister(BaseModel):
    email: EmailStr
    password: str


class SVerifyPhone(BaseModel):
    phone_number: str
