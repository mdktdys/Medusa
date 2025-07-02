from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from src.alchemy.db_helper import AsyncSession, db_helper
from . import crud
from .schemas import ZamenaResponse, ZamenaRequest


namespace: str = 'zamena_router'
router = APIRouter(tags=[namespace])


@router.get("/zamena", response_model = ZamenaResponse)
@cache(expire = 6000, namespace = namespace)
async def get_zamena(request: ZamenaRequest, session: AsyncSession = Depends(db_helper.session_dependency)) -> ZamenaResponse:
    return crud.get_zamena(session = session, request = request)
