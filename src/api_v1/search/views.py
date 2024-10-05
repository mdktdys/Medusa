from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.alchemy.db_helper import *
from . import crud
from .schemas import SearchResult
from ...auth.auth import any_auth_method

router = APIRouter(tags=["Search"])


@router.get("/search/{query}/")
async def get_search(
    query: str, session: AsyncSession = Depends(db_helper.session_dependency)
) -> List[SearchResult]:
    return await crud.get_search_items(session=session, search_filter=query)
