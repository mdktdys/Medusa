from celery.result import AsyncResult
from pydantic import BaseModel


class TaskCreatedResponse(BaseModel):
    task_id: str
    status: str = "PENDING"
    detail_url: str | None = None

    @classmethod
    def from_async_result(cls, result: AsyncResult) -> "TaskCreatedResponse":
        return cls(
            task_id = result.id, # type: ignore
            status = result.status,
        )
