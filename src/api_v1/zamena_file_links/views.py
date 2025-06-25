from typing import List
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from fastapi import Query
from datetime import date
from src.alchemy.db_helper import AsyncSession, db_helper
from . import crud 
from .schemas import ZamenaFileLink, ZamenaFileLinksFilter

namespace: str = 'zamena_file_links'
router = APIRouter(tags=[namespace])


@router.get("/", response_model = List[ZamenaFileLink])
@cache(expire = 6000, namespace = namespace)
async def get_zamena_file_links(
    start_date: date = Query(None),
    end_date: date = Query(None),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> List[ZamenaFileLink]:
    filter = ZamenaFileLinksFilter(
        start_date = start_date,
        end_date = end_date,
    )
    return await crud.get_zamena_file_links(session = session, filter = filter)