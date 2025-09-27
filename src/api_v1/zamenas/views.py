from typing import List
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from src.auth.auth import any_auth_method
from src.alchemy.db_helper import AsyncSession, local_db_helper
from . import crud 
from .schemas import ZamenaFilter, CreateZamenaRequest, ZamenaSwap, ZamenaGroup

namespace: str = 'zamenas'
router = APIRouter(tags=[namespace])


@router.get('/')
@cache(expire = 6000, namespace = namespace)
async def get_zamenas(
    filter: ZamenaFilter = Depends(),
    session: AsyncSession = Depends(local_db_helper.session_dependency),
):
    return await crud.get_amenas(session = session, filter = filter)


@router.post('/', dependencies=[Depends(any_auth_method(roles=['Owner']))])
async def create_zamena(
    request: CreateZamenaRequest,
    session: AsyncSession = Depends(local_db_helper.session_dependency),
):
    return await crud.create_zamena(session = session, request = request)


@router.post('/swaps', dependencies=[Depends(any_auth_method(roles=['Owner']))])
async def create_zamena_swaps(
    request: List[ZamenaSwap],
    session: AsyncSession = Depends(local_db_helper.session_dependency),
):
    return await crud.create_zamena_swaps(session = session, request = request)


@router.post('/group', dependencies=[Depends(any_auth_method(roles=['Owner']))])
async def create_zamena_group(
    request: List[ZamenaGroup],
    session: AsyncSession = Depends(local_db_helper.session_dependency),
):
    return await crud.create_zamena_group(session = session, request = request)