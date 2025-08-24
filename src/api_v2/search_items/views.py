from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.alchemy.database_local import SearchItem
from src.alchemy.db_helper import AsyncSession, local_db_helper
from src.api_v2.search_items import crud

from .schemas import SearchItemDto

namespace: str = 'SeachItems'
router = APIRouter(tags = [namespace])
@router.get("/", response_model = List[SearchItemDto])
@cache(expire = 6000, namespace = namespace)
async def get_groups(session: AsyncSession = Depends(local_db_helper.session_dependency)) -> List[SearchItem]:
    return await crud.get_seach_items(session = session)