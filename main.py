from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from src.alchemy import *
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from src.api_v1 import router as router_v1
from src.core.config import settings
from fastapi_cache.decorator import cache


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # redis = aioredis.from_url("redis://localhost")
    redis = aioredis.from_url("redis://redis")
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    print("end")


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


@app.get("/")
@cache(expire=60)
async def index():
    return dict(hello="a")


# @app.get("/next/{group_id}/{form}")
# def read_root(group_id: int = 2533,form : str = "formated"):
#     if form == 'formated':
#         res = get_group_default_schedule_formatted(group_id, 33)
#         return res
#     if form == 'json':
#         res = get_group_default_schedule(group_id, 33)
#         return res[get_next_day_number()]


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
