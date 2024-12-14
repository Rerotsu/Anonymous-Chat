
from typing import Literal
from dotenv import load_dotenv
from pydantic import Field, ValidationInfo, field_validator
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"] = Field(..., env="MODE")
    LOG_LEVEL: str = Field(..., env="LOG_LEVEL")

    DB_HOST: str = Field(..., env="DB_HOST")
    DB_PORT: int = Field(..., env="DB_PORT")
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASS: str = Field(..., env="DB_PASS")
    DB_NAME: str = Field(..., env="DB_NAME")
    DATABASE_URL: str = ""

    @field_validator('DATABASE_URL', mode='before')
    def assemble_db_connection(cls, v, info: ValidationInfo):
        values = info.data
        return f"postgresql+asyncpg://{values['DB_USER']}:{values['DB_PASS']}@{values['DB_HOST']}:{values['DB_PORT']}/{values['DB_NAME']}"

    SMTP_HOST: str = Field(..., env="SMTP_HOST")
    SMTP_PORT: int = Field(..., env="SMTP_PORT")
    SMTP_USER: str = Field(..., env="SMTP_USER")
    SMTP_PASS: str = Field(..., env="SMTP_PASS")

    TWILIO_ACCOUNT_SID: str = Field(..., env="TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN: str = Field(..., env="TWILIO_AUTH_TOKEN")
    NUMBER: str = Field(..., env="NUMBER")

    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field(..., env="ALGORITHM")

    class Config:
        env_file = ".env"  # Укажите файл конфигурации
        extra = 'allow'


settings = Settings()
