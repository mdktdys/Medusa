from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.alchemy.db_helper import AsyncSession, db_helper

from .crud import get_full_data
from .schemas import FullDataDto

namespace: str = 'data_router'
router = APIRouter(tags=[namespace])


@router.get("/full", response_model = FullDataDto)
@cache(expire = 6000, namespace = namespace)
async def get_data(session: AsyncSession = Depends(db_helper.session_dependency)) -> FullDataDto:
    return FullDataDto()


@router.post('/fetch', response_model = str)
async def fetch_data(session: AsyncSession = Depends(db_helper.session_dependency)):
    return ''