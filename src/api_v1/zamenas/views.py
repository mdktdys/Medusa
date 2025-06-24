from typing import List, Union
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from fastapi import Query
from datetime import date
from src.alchemy.db_helper import AsyncSession, db_helper
from . import crud 
from .schemas import Zamena, ZamenaFilter

namespace: str = 'zamenas'
router = APIRouter(tags=[namespace])


@router.get("/", response_model = List[Zamena])
@cache(expire = 6000, namespace = namespace)
async def get_zamenas(
    group: Union[List[int], None] = Query(default=None),
    number: int = Query(None),
    course: int = Query(None),
    teacher: int = Query(None),
    cabinet: int = Query(None),
    id: int = Query(None),
    start_date: date = Query(None),
    end_date: date = Query(None),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> List[Zamena]:
    filter = ZamenaFilter(
        group = group,
        number = number,
        course = course,
        teacher = teacher,
        cabinet = cabinet,
        id = id,
        start_date = start_date,
        end_date = end_date,
    )
    return await crud.get_zamenas(session = session, filter = filter)