from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.alchemy.db_helper import AsyncSession, local_db_helper

from . import crud

router = APIRouter(tags=["Disciplines"])


@router.get("/")
@cache(expire = 6000)
async def get_teachers(session: AsyncSession = Depends(local_db_helper.session_dependency)):
    return await crud.get_disciplines(session = session)