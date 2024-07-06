from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Union

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from src.core.tools import get_next_day_number
from src.core.schedule_api import get_group_default_schedule, get_group_default_schedule_formatted

from redis import asyncio as aioredis


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

app = FastAPI(lifespan=lifespan)


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