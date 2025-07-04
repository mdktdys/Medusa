from typing import List
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from src.alchemy.db_helper import AsyncSession, db_helper
from . import crud 
from .schemas import Timing


namespace: str = 'timings'
router = APIRouter(tags=[namespace])


@router.get("/", response_model = List[Timing])
@cache(expire = 6000, namespace = namespace)
async def get_timings(session: AsyncSession = Depends(db_helper.session_dependency)) -> List[Timing]:
    return await crud.get_timings(session = session)

