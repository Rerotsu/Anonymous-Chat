from typing import Literal
from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DATABASE_URL: str = ""

    @field_validator("DATABASE_URL", mode="before")
    def assemble_db_connection(cls, v, info: ValidationInfo):
        values = info.data
        return f"postgresql+asyncpg://{values['DB_USER']}:{values['DB_PASS']}@{values['DB_HOST']}:{values['DB_PORT']}/{values['DB_NAME']}"

    SMTP_HOST: str
    SMTP_PORT: str
    SMTP_USER: str
    SMTP_PASS: str

    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    NUMBER: str

    SECRET_KEY: str
    ALGHORITHM: str

    class Config:
        extra = 'allow'


settings = Settings()
