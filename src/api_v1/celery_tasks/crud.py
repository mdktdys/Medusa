from celery.result import AsyncResult
from sqlalchemy.ext.asyncio import AsyncSession

from src.parser.tasks import parser_celery_app

from .schemas import TaskRequest, TaskResponse


async def get_task(session: AsyncSession, request: TaskRequest) -> TaskResponse:
    res: AsyncResult = AsyncResult(request.task_id, app = parser_celery_app)
    return TaskResponse.from_async_result(res)