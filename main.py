from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from redis.asyncio.client import Redis
from starlette.middleware.cors import CORSMiddleware

from my_secrets import REDIS_PASSWORD
from router import description, router, tags_metadata
from src.alchemy import Base, db_helper
from src.alchemy.database_local import Base as LocalBase
from src.alchemy.db_helper import local_db_helper
from src.utils.key_builder import default_key_builder


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis: Redis = aioredis.from_url(
        f"redis://:{REDIS_PASSWORD}@redis:6379/1",
        decode_responses=False
    )

    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with local_db_helper.engine.begin() as conn:
        await conn.run_sync(LocalBase.metadata.create_all)

    FastAPICache.init(
        RedisBackend(redis),
        prefix = 'fastapi-cache',
        key_builder = default_key_builder
    )
    yield


app = FastAPI(
    swagger_ui_parameters = {'syntaxHighlight.theme': 'obsidian'},
    title = 'API 🐋 Замены уксивтика',
    openapi_tags = tags_metadata,
    description = description,
    lifespan = lifespan,
    docs_url = '/',
    contact={
        'name': 'telegram: @mdktdys',
        'url': 'https://uksivt.xyz',
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

app.include_router(router = router)
