
from fastapi import APIRouter, Depends
from fastapi_cache import FastAPICache

from src.alchemy.db_helper import AsyncSession, db_helper, local_db_helper
from . import crud

router = APIRouter(tags=["Manage"])


@router.get("/sync_local_database", response_model=dict)
async def sync_local_database(
        supabase_session: AsyncSession = Depends(db_helper.session_dependency),
        local_session: AsyncSession = Depends(local_db_helper.session_dependency),
) -> dict:
    return await crud.sync_local_database(supabase_session, local_session)


@router.delete('purge_cache', response_model = dict)
def purge_cache():
        FastAPICache.reset()
        return {
                'result': 'ok'
        }
        