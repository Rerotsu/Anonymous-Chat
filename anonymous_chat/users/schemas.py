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

    @field_validator('confirm_password')
    def passwords_match(cls, v, values):
        password = getattr(values, 'password', None)
        if password is not None and v != password:
            raise ValueError('Пароли не совпадают')
        return v


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
