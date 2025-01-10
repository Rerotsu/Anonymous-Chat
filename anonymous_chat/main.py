
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from anonymous_chat.users.router import router as user_router
from anonymous_chat.chats.router import router as chat_router
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
app.include_router(page_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
