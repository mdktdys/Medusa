from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.alchemy.db_helper import *
from . import crud

router = APIRouter(tags=["search"])


@router.get("/search/{query}/")
@cache(expire=60)
async def get_search(
    query: str, session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.get_search_items(session=session, search_filter=query)
