from typing import Literal
from pydantic import ConfigDict, ValidationInfo, field_validator
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

    SECRET_KEY: str
    ALGHORITHM: str

    model_config = ConfigDict(env_file=".env", arbitrary_types_allowed=True)


settings = Settings()
