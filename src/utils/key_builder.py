from typing import Callable, Optional

from fastapi import Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.logger import logger


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

    args_repr = ",".join(map(str, args or ()))
    kwargs_repr = ",".join(f"{k}={v}" for k, v in safe_kwargs.items())
    
    key: str = f'{namespace}:{func.__module__}.{func.__name__}?args={args_repr}&kwargs={kwargs_repr}'
    if request is not None:
        logger.info(f'🗑️ Сохранен {request.url} в кеш с ключем {key}')

    return key

