from fastapi import APIRouter, Depends
from src.api_v1 import router as api_v1_router
from src.auth.auth import router as auth_router, any_auth_method

router = APIRouter()

router.include_router(
    auth_router,
    include_in_schema = False,
    prefix="/auth",
)

router.include_router(
    api_v1_router,
    prefix="/api/v1",
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