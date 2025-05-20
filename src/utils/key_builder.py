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
    safe_kwargs = {
        k: v for k, v in (kwargs or {}).items()
        if not isinstance(v, AsyncSession)
    }

    prefix = f"{FastAPICache.get_prefix()}:{namespace}:"
    args_repr = ",".join(map(str, args or ()))
    kwargs_repr = ",".join(f"{k}={v}" for k, v in safe_kwargs.items())

    return f"{prefix}{func.__module__}.{func.__name__}?args={args_repr}&kwargs={kwargs_repr}"

