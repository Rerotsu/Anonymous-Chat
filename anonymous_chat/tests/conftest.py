from datetime import datetime
import json
import pytest_asyncio
from sqlalchemy import insert, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from anonymous_chat.config import settings
from anonymous_chat.database import async_session_maker, Base
from anonymous_chat.users.models import User

# Создание асинхронного движка и сессии
async_engine = create_async_engine(settings.TEST_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # def open_mock_json(model: str):
    #     with open(f"anonymous_chat/tests/mock_{model}.json", "r") as file:
    #         data = json.load(file)
    #         for user in data:
    #             if 'created' in user:
    #                 user['created'] = datetime.fromisoformat(user['created'])
    #         return data
        
    # users = open_mock_json("users")

    # async with async_session_maker() as session:
    #     for user in users:
    #         await session.execute(insert(User).values(user))
    #     await session.commit()

    yield print("True")


@pytest_asyncio.fixture(scope="function")
async def session():
    async with AsyncSessionLocal() as session:
        yield session
        await session.commit()


# @pytest_asyncio.fixture(scope="function")
# async def reset_users_table(session):
#     await session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE;"))
#     await session.commit()
