from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.alchemy.db_helper import AsyncSession, db_helper
from . import crud
from .schemas import Course

namespace: str = 'Courses'
router = APIRouter(tags=[namespace])


@router.get("/", response_model = list[Course])
@cache(expire = 6000, namespace = namespace)
async def get_groups(session: AsyncSession = Depends(db_helper.session_dependency)) -> List[Course]:
    return await crud.get_courses(session=session)