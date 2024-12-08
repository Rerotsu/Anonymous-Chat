from pydantic import BaseModel, EmailStr, PhoneNumber


class SUserRegister(BaseModel):
    email: EmailStr
    phone_number = PhoneNumber
    password: str


class SVerifyPhone(BaseModel):
    phone_number: PhoneNumber
    code: str
