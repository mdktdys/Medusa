from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from src.alchemy import *
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from src.api_v1 import router as router_v1
from src.core.config import settings


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(
        "redis://redis",
        decode_responses=False,
        encoding="utf8",
    )
    redis_data = await redis.keys()
    print(redis_data)
    for key in redis_data:
        print(f"{key}")
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(lifespan=lifespan, docs_url="/")
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)
