from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.alchemy.db_helper import *
from . import crud
from .schemas import (
    Cabinet,
)

router = APIRouter(tags=["Cabinets"])


@router.get("/", response_model=list[Cabinet])
@cache(expire=6000)
async def get_cabinets(session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.get_cabinets(session=session)


@router.get("/id/{cabinet_id}/", response_model=list[Cabinet])
@cache(expire=6000)
async def get_cabinet_by_id(
    cabinet_id: int = -1,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_cabinet_by_id(session=session, cabinet_id=cabinet_id)
