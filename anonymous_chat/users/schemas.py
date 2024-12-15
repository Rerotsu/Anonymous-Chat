import phonenumbers
from pydantic import BaseModel, EmailStr, field_validator


class SUserRegister(BaseModel):
    email: EmailStr
    phone_number: str
    password: str
    confirm_password: str

    @field_validator('phone_number')
    def validate_phone_number(cls, value):
        try:
            phone = phonenumbers.parse(value)
            if not phonenumbers.is_valid_number(phone):
                raise ValueError("Неверный номер телефона(неверный телефонный индекс)")
            return value
        except phonenumbers.NumberParseException:
            raise ValueError("Неверный формат номера телефона")


class SVerifyPhone(BaseModel):
    phone_number: str
    code: str

    @field_validator('phone_number')
    def validate_phone_number(cls, value):
        try:
            phone = phonenumbers.parse(value)
            if not phonenumbers.is_valid_number(phone):
                raise ValueError("Неверный номер телефона")
            return value
        except phonenumbers.NumberParseException:
            raise ValueError("Неверный формат номера телефона")
