from celery.result import AsyncResult

from .schemas import TaskRequest, TaskResponse


async def get_task(request: TaskRequest) -> TaskResponse:
    from src.parser.tasks import parser_celery_app
    res: AsyncResult = AsyncResult(request.task_id, app = parser_celery_app)
    return TaskResponse.from_async_result(res)