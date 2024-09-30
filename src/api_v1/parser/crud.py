import asyncio

from fastapi import HTTPException

from fastapicelery import fastapi_celery_app


async def get_latest_zamena_link():
    # Отправляем задачу в Celery
    task = fastapi_celery_app.send_task("broker.get_latest_zamena_link")

    # Используем asyncio для асинхронного ожидания результата
    result = await asyncio.to_thread(task.get, timeout=60)

    if result:
        return result
    else:
        raise HTTPException(
            status_code=500, detail="Task failed or result not available"
        )
