from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.alchemy.db_helper import *
from . import crud
from .schemas import Group

router = APIRouter(tags=["Groups"])


@router.get("/", response_model=list[Group])
@cache(expire=60)
async def get_groups(session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.get_groups(session=session)


@router.get("/group/{group_id}/", response_model=list[Group])
@cache(expire=60)
async def get_group_by_id(
    group_id: int = -1, session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.get_group_by_id(session=session, group_id=group_id)
