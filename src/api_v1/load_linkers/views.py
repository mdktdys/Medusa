from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy.db_helper import local_db_helper
from src.auth.auth import any_auth_method

from . import crud
from .schemas import (CreateLoadLinkRequest, DeleteLoadLinkRequest,
                      LoadLinkersRequest)

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
    

@router.post(
    '/',
    dependencies=[Depends(any_auth_method(roles=['Owner']))]
)
async def create_load_link(
    request: CreateLoadLinkRequest,
    session: AsyncSession = Depends(local_db_helper.session_dependency)
):
    return await crud.create_load_link(
        request = request,
        session = session
    )
    
    
@router.delete(
    '/',
    dependencies=[Depends(any_auth_method(roles=['Owner']))]
)
async def delete_load_link(
    request: DeleteLoadLinkRequest,
    session: AsyncSession = Depends(local_db_helper.session_dependency)
):
    return await crud.delete_load_link(
        request = request,
        session = session
    )