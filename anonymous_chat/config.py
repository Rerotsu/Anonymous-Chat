from typing import Literal
from dotenv import load_dotenv
from pydantic import ConfigDict, Field, ValidationInfo, field_validator
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"] = Field(..., json_schema_extra={"env": "MODE"})
    LOG_LEVEL: str = Field(..., json_schema_extra={"env": "LOG_LEVEL"})

    DB_HOST: str = Field(..., json_schema_extra={"env": "DB_HOST"})
    DB_PORT: int = Field(..., json_schema_extra={"env": "DB_PORT"})
    DB_USER: str = Field(..., json_schema_extra={"env": "DB_USER"})
    DB_PASS: str = Field(..., json_schema_extra={"env": "DB_PASS"})
    DB_NAME: str = Field(..., json_schema_extra={"env": "DB_NAME"})
    DATABASE_URL: str = ""

    @field_validator("DATABASE_URL", mode="before")
    def assemble_db_connection(cls, v, info: ValidationInfo):
        values = info.data
        return f"postgresql+asyncpg://{values['DB_USER']}:{values['DB_PASS']}@{values['DB_HOST']}:{values['DB_PORT']}/{values['DB_NAME']}"

    TEST_DB_HOST: str = Field(..., json_schema_extra={"env": "TEST_DB_HOST"})
    TEST_DB_PORT: int = Field(..., json_schema_extra={"env": "TEST_DB_PORT"})
    TEST_DB_USER: str = Field(..., json_schema_extra={"env": "TEST_DB_USER"})
    TEST_DB_PASS: str = Field(..., json_schema_extra={"env": "TEST_DB_PASS"})
    TEST_DB_NAME: str = Field(..., json_schema_extra={"env": "TEST_DB_NAME"})
    TEST_DATABASE_URL: str = ""

    @field_validator("TEST_DATABASE_URL", mode="before")
    def assemble_test_db_connection(cls, v, info: ValidationInfo):
        values = info.data
        return f"postgresql+asyncpg://{values['TEST_DB_USER']}:{values['TEST_DB_PASS']}@{values['TEST_DB_HOST']}:{values['TEST_DB_PORT']}/{values['TEST_DB_NAME']}"

    SMTP_HOST: str = Field(..., json_schema_extra={"env": "SMTP_HOST"})
    SMTP_PORT: int = Field(..., json_schema_extra={"env": "SMTP_PORT"})
    SMTP_USER: str = Field(..., json_schema_extra={"env": "SMTP_USER"})
    SMTP_PASS: str = Field(..., json_schema_extra={"env": "SMTP_PASS"})

    TWILIO_ACCOUNT_SID: str = Field(
        ..., json_schema_extra={"env": "TWILIO_ACCOUNT_SID"}
    )
    TWILIO_AUTH_TOKEN: str = Field(..., json_schema_extra={"env": "TWILIO_AUTH_TOKEN"})
    NUMBER: str = Field(..., json_schema_extra={"env": "NUMBER"})

    SECRET_KEY: str = Field(..., json_schema_extra={"env": "SECRET_KEY"})
    ALGORITHM: str = Field(..., json_schema_extra={"env": "ALGORITHM"})

    model_config = ConfigDict(env_file=".env", extra="allow")


settings = Settings()
