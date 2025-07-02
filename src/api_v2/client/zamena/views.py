from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from src.alchemy.db_helper import AsyncSession, db_helper
from . import crud
from .schemas import ZamenaResponse, ZamenaRequest
from datetime import date

namespace: str = 'zamena_router'
router = APIRouter(tags=[namespace])


@router.get("/", response_model = ZamenaResponse)
@cache(expire = 6000, namespace = namespace)
async def get_zamena(date_from: date, date_to: date, session: AsyncSession = Depends(db_helper.session_dependency)) -> ZamenaResponse:
    return await crud.get_zamena(session = session, request = ZamenaRequest(date_from = date_from, date_to = date_to))
