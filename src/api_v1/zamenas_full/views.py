from typing import List, Union
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from fastapi import Query
from datetime import date
from src.alchemy.db_helper import AsyncSession, db_helper
from . import crud 
from .schemas import ZamenasFull, ZamenasFullFilter

namespace: str = 'zamenas_full'
router = APIRouter(tags=[namespace])


@router.get("/", response_model = List[ZamenasFull])
@cache(expire = 6000, namespace = namespace)
async def get_zamenas_full(
    group: Union[List[int], None] = Query(default=None),
    id: int = Query(None),
    start_date: date = Query(None),
    end_date: date = Query(None),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> List[ZamenasFull]:
    filter = ZamenasFullFilter(
        group = group,
        id = id,
        start_date = start_date,
        end_date = end_date,
    )
    return await crud.get_zamenas_full(session = session, filter = filter)