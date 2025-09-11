from fastapi import APIRouter

from src.api_v1 import router as api_v1_router
from src.api_v2.router import router as api_v2_router
from src.auth.views import router as auth_router

router = APIRouter()

router.include_router(
    auth_router,
    prefix = '/auth',
)

router.include_router(
    api_v1_router,
    prefix = '/v1',
)

router.include_router(
    api_v2_router,
    prefix = '/v2'
)

tags_metadata: list[dict[str, str]] = []

description = '''
Публичный API для получения информации об расписании

# Нотификации
## ClientID
1 - Web подписчики
2 - Android подписчики

## subType
1 - Группы
2 - Преподаватели
3 - Кабинеты
'''