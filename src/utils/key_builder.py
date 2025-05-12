import hashlib
import json
from fastapi import Request
from typing import Callable
import inspect
from sqlalchemy.ext.asyncio import AsyncSession

def custom_key_builder(
    func: Callable,
    namespace: str,
    request: Request,
    *args,
    **kwargs
) -> str:
    sig = inspect.signature(func)
    bound = sig.bind_partial(*args, **kwargs)
    bound.apply_defaults()

    # Исключаем параметры типа AsyncSession (и другие потенциально нестабильные объекты)
    safe_args = {
        k: v for k, v in bound.arguments.items()
        if not isinstance(v, AsyncSession)
    }

    raw_key = f"{namespace}:{request.url.path}:{json.dumps(safe_args, sort_keys=True, default=str)}"
    return f"{namespace}:{hashlib.md5(raw_key.encode()).hexdigest()}"