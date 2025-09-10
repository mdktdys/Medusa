from fastapi import APIRouter, Depends

from src.alchemy.db_helper import AsyncSession, db_helper

from . import crud
from .schemas import TaskRequest, TaskResponse

namespace: str = 'Tasks'
router = APIRouter(tags=[namespace])

@router.get("/")
async def get_task(
    request: TaskRequest = Depends(),
    session: AsyncSession = Depends(db_helper.session_dependency)
) -> TaskResponse:
    return await crud.get_task(
        session = session,
        request = request
    )