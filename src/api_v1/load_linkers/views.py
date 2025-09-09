from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy.db_helper import local_db_helper

from . import crud
from .schemas import LoadLinkersRequest

namespace: str = 'LoadLinkers'
router = APIRouter(tags=[namespace])

@router.get('/')
async def get_load_linkers(
    request: LoadLinkersRequest = Depends(),
    session: AsyncSession = Depends(local_db_helper.session_dependency)
):
    return await crud.get_load_linkers(
        request = request,
        session = session,
    )