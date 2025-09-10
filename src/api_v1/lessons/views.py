from datetime import date
from typing import List, Union

from fastapi import APIRouter, Depends, Query
from fastapi_cache.decorator import cache

from src.alchemy.db_helper import AsyncSession, db_helper, local_db_helper
from src.auth.auth import any_auth_method

from . import crud
from .schemas import Lesson, LessonFilter

namespace: str = 'lessons'
router = APIRouter(tags=[namespace])


@router.get("/", response_model = List[Lesson])
@cache(expire = 6000, namespace = namespace)
async def get_lessons(
    group: Union[List[int], None] = Query(default=None),
    number: int = Query(None),
    course: int = Query(None),
    teacher: int = Query(None),
    cabinet: int = Query(None),
    id: int = Query(None),
    start_date: date = Query(None),
    end_date: date = Query(None),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> List[Lesson]:
    filter = LessonFilter(
        group = group,
        number = number,
        course = course,
        teacher = teacher,
        cabinet = cabinet,
        id = id,
        start_date = start_date,
        end_date = end_date,
    )
    return await crud.get_lessons(session = session, filter = filter)


@router.post(
    '/',
    dependencies=[Depends(any_auth_method(roles=['Owner']))]
)
async def create_lessons(
    request: List[Lesson],
    session: AsyncSession = Depends(local_db_helper.session_dependency)
):
    return await crud.create_lessons(session = session, request = request)