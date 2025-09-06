from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy.db_helper import local_db_helper

from . import crud
from .schemas import SpecializationsResponse

router = APIRouter(tags=['Specializations'])

@router.get('/', response_model = SpecializationsResponse)
@cache(expire = 6000)
async def get_specializations(session: AsyncSession = Depends(local_db_helper.session_dependency)) -> SpecializationsResponse:
    return await crud.get_specializations(session = session)