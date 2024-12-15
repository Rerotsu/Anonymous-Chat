
from fastapi import FastAPI

from anonymous_chat.users.router import router as user_router
from anonymous_chat.chats.router import router as chat_router
from anonymous_chat.chats.messages.router import router as message_router
from anonymous_chat.pages.router import router as page_router


"""
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8", decode_responses=True
        )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
"""

app = FastAPI()

app.include_router(user_router)
app.include_router(chat_router)
app.include_router(message_router)
app.include_router(page_router)
