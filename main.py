import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi.openapi.docs import get_swagger_ui_html

from src.alchemy import *
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from src.api_v1 import router as router_v1
from src.core.config import settings
from router import router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://redis", decode_responses=False)
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(
    lifespan=lifespan,
    docs_url="/",
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
)

app.include_router(router=router)


@app.get("/", include_in_schema=False)
async def custom_swagger_ui_html_cdn():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        swagger_css_url="https://cdn.jsdelivr.net/gh/Itz-fork/Fastapi-Swagger-UI-Dark/assets/swagger_ui_dark.min.css",
    )
