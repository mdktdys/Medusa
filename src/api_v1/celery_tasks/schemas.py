from typing import Any, Optional

from celery.result import AsyncResult
from pydantic import BaseModel


class TaskCreatedResponse(BaseModel):
    task_id: str
    status: str = "PENDING"

    @classmethod
    def from_async_result(cls, result: AsyncResult) -> "TaskCreatedResponse":
        return cls(
            task_id = result.id, # type: ignore
            status = result.status,
        )


class TaskRequest(BaseModel):
    task_id: str
    

class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Any] = None
    error: Optional[str] = None

    @classmethod
    def from_async_result(cls, result: AsyncResult) -> "TaskResponse":
        response = cls(
            task_id=result.id,  # type: ignore
            status=result.status,
        )

        if result.successful():
            response.result = result.result
        elif result.failed():
            response.error = str(result.result)

        return response