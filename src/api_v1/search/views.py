from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.alchemy.db_helper import *
from . import crud
from .schemas import SearchResult

router = APIRouter(tags=["search"])


@router.get("/search/{query}/")
@cache(expire=600)
async def get_search(
    query: str, session: AsyncSession = Depends(db_helper.session_dependency)
) -> List[SearchResult]:
    return await crud.get_search_items(session=session, search_filter=query)
