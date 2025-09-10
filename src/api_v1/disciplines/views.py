from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.alchemy.db_helper import AsyncSession, local_db_helper
from src.auth.auth import any_auth_method

from . import crud
from .schemas import CreateDisciplineAliasRequest, DisciplineAliasesRequest

router = APIRouter(tags = ['Disciplines'])


@router.get('/')
@cache(expire = 6000)
async def get_disciplines(session: AsyncSession = Depends(local_db_helper.session_dependency)):
    return await crud.get_disciplines(session = session)


@router.get('/codes/')
@cache(expire = 6000)
async def get_disciplines_codes(session: AsyncSession = Depends(local_db_helper.session_dependency)):
    return await crud.get_disciplines_codes(session = session)


@router.get('/alias')
async def get_discipline_aliases(request: DisciplineAliasesRequest = Depends(), session: AsyncSession = Depends(local_db_helper.session_dependency)):
    return await crud.get_discipline_aliases(request = request,session = session)

@router.post(
    '/alias',
    dependencies=[Depends(any_auth_method(roles=['Owner']))]
)
async def create_discipline_alias(request: CreateDisciplineAliasRequest, session: AsyncSession = Depends(local_db_helper.session_dependency)):
    return await crud.create_discipline_alias(request = request, session = session)