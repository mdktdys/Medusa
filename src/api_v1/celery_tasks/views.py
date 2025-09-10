from fastapi import APIRouter, Depends

from . import crud
from .schemas import TaskRequest, TaskResponse

namespace: str = 'Tasks'
router = APIRouter(tags=[namespace])

@router.get('/')
async def get_task(request: TaskRequest = Depends()) -> TaskResponse:
    return await crud.get_task(request = request)