from typing import Tuple

from fastapi import HTTPException
from src.api_v1.departments.schemas import Department
from src.alchemy.db_helper import AsyncSession
from sqlalchemy import Select, select, Result
from src.alchemy import database
from .schemas import DepartmentCreate

async def get_departments(session: AsyncSession) -> list[Department]:
    query: Select[Tuple[database.Departments]] = select(database.Departments)
    result: Result = await session.execute(query)
    return list(result.scalars().all())


async def get_department_by_id(session: AsyncSession, department_id: int) -> Department:
    query: Select[Tuple[database.Departments]] = select(database.Departments).where(database.Departments.id == department_id)
    result: Result[Tuple[database.Departments]] = await session.execute(query)
    department: database.Departments | None = result.scalar_one_or_none()

    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")

    return department # type: ignore

async def update_department(
    session: AsyncSession,
    department_id: int,
    data: Department
) -> Department:
    query: Select[Tuple[database.Departments]] = select(database.Departments).where(database.Departments.id == department_id)
    result: Result[Tuple[database.Departments]] = await session.execute(query)
    department: database.Departments | None = result.scalar_one_or_none()

    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(department, key, value)

    await session.commit()
    await session.refresh(department)
    return department # type: ignore


async def delete_department(session: AsyncSession, department_id: int) -> dict[str, str]:
    query: Select[Tuple[database.Departments]] = select(database.Departments).where(database.Departments.id == department_id)
    result: Result[Tuple[database.Departments]] = await session.execute(query)
    department: database.Departments | None = result.scalar_one_or_none()

    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")

    await session.delete(department)
    await session.commit()
    return {"result": "ok"}


async def create_department(session: AsyncSession, data: DepartmentCreate) -> Department:
    new_department = database.Departments(**data.model_dump(exclude={"id"}))
    session.add(new_department)
    await session.commit()
    await session.refresh(new_department)
    return new_department # type: ignore