from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from starlette.middleware.cors import CORSMiddleware

from src.alchemy import *
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from src.alchemy.db_helper import local_db_helper
from router import router, tags_metadata, description


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://redis", decode_responses=False)
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with local_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(
    title = 'API 🐋 Замены уксивтика',
    openapi_tags = tags_metadata,
    description = description,
    contact={
        "name": "telegram: @mdktdys",
        "url": "https://uksivt.xyz",
    },
    lifespan=lifespan,
    docs_url="/",
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

app.include_router(router=router)
