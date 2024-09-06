from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.alchemy.db_helper import *
from . import crud
from .schemas import SearchResult

router = APIRouter(tags=["Search"])


@router.get("/search/{query}/")
@cache(expire=6000)
async def get_search(
    query: str, session: AsyncSession = Depends(db_helper.session_dependency)
) -> List[SearchResult]:
    return await crud.get_search_items(session=session, search_filter=query)
