from typing import List
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from fastapi import Query
from datetime import date
from src.alchemy.db_helper import AsyncSession, db_helper
from . import crud 
from .schemas import AlreadyFoundLink, AlreadyFoundLinkFilter

namespace: str = 'already_found_links'
router = APIRouter(tags=[namespace])


@router.get("/", response_model = List[AlreadyFoundLink])
@cache(expire = 6000, namespace = namespace)
async def get_already_found_links(
    start_date: date = Query(None),
    end_date: date = Query(None),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> List[AlreadyFoundLink]:
    filter = AlreadyFoundLinkFilter(
        start_date = start_date,
        end_date = end_date,
    )
    return await crud.get_already_found_links(session = session, filter = filter)