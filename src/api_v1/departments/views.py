from fastapi import APIRouter, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from src.alchemy.db_helper import db_helper, AsyncSession
from .schemas import Department, DepartmentCreate
from . import crud
from src.auth.auth import any_auth_method

namespace: str = 'Departments'
router = APIRouter(tags=[namespace])


@router.get("/", response_model = list[Department])
@cache(expire=60000, namespace = namespace)
async def get_departments(session: AsyncSession = Depends(db_helper.session_dependency)) -> list[Department]:
    return await crud.get_departments(session=session)


@router.get("/{department_id}", response_model = Department)
@cache(expire=60000, namespace = namespace)
async def get_department_by_id(
    department_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Department:
    return await crud.get_department_by_id(session=session, department_id=department_id)


@router.put("/{department_id}", response_model = Department, dependencies = [Depends(any_auth_method(roles=["Owner"]))])
async def update_department(
    department_id: int,
    data: Department,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Department:
    result: Department = await crud.update_department(session, department_id, data)
    await FastAPICache.clear(namespace = namespace)
    return result


@router.delete("/{department_id}", dependencies = [Depends(any_auth_method(roles=["Owner"]))])
async def delete_department(
    department_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> dict[str, str]:
    result: dict[str, str] = await crud.delete_department(session, department_id)
    await FastAPICache.clear(namespace = namespace)
    return result


@router.post("/", response_model = Department, status_code=201, dependencies = [Depends(any_auth_method(roles=["Owner"]))])
async def create_department(
    data: DepartmentCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Department:
    result: Department = await crud.create_department(session=session, data=data)
    await FastAPICache.clear(namespace = namespace)
    return result