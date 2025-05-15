import hashlib
from typing import Callable, Optional
from fastapi import Request, Response
from fastapi_cache import FastAPICache
from sqlalchemy.ext.asyncio import AsyncSession

def default_key_builder(
    func: Callable,
    namespace: Optional[str] = "",
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
) -> str:
    print('ARGS')
    print(args)
    print('KWARGS')
    print(kwargs)

    # Фильтруем из kwargs значения, которые не сериализуются (например, AsyncSession)
    safe_kwargs = {
        k: v for k, v in (kwargs or {}).items()
        if not isinstance(v, AsyncSession)
    }

    prefix = f"{FastAPICache.get_prefix()}:{namespace}:"
    cache_key = (
        prefix
        + hashlib.md5(
            f"{func.__module__}:{func.__name__}:{args}:{safe_kwargs}".encode()
        ).hexdigest()
    )
    return cache_key

