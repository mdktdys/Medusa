import asyncio
import datetime
from typing import List

import celery.exceptions
from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from fastapicelery import fastapi_celery_app
from src.alchemy import database
from src.api_v1.parser.schemas import ParseZamenaRequest


async def parse_zamena(request: ParseZamenaRequest):
    url = request.url
    date = request.date
    try:
        # Отправляем задачу в Celery
        task = fastapi_celery_app.send_task(
            "parser.tasks.parse_zamena",
            args=[url, date],
            retry=True,
            retry_policy={
                "max_retries": 5,
                "interval_start": 1,
                "interval_step": 1,
                "interval_max": 10,
                "retry_errors": None,
            },
        )

        # Ожидаем результат задачи, используя asyncio.to_thread для выполнения task.get() в отдельном потоке
        result = await asyncio.to_thread(task.get, timeout=60)

        # Проверяем результат
        if result:
            return result
        else:
            raise HTTPException(
                status_code=500, detail="Task completed but returned no result"
            )

    except celery.exceptions.TimeoutError:
        # В случае, если задача не завершилась в пределах таймаута
        raise HTTPException(status_code=504, detail="Celery task timed out")

    except Exception as e:
        # Для всех остальных исключений
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the task: {str(e)}",
        )


async def get_latest_zamena_link():
    # Отправляем задачу в Celery
    task = fastapi_celery_app.send_task("parser.tasks.get_latest_zamena_link")

    result = await asyncio.to_thread(task.get, timeout=60)

    if result:
        return result
    else:
        raise HTTPException(
            status_code=500, detail="Task failed or result not available"
        )


async def check_new(session: AsyncSession):
    # Отправляем задачу в Celery
    task = fastapi_celery_app.send_task("parser.tasks.check_new")

    # Используем asyncio для асинхронного ожидания результата
    result = await asyncio.to_thread(task.get, timeout=60)

    # values = [{"link": link} for link in result]

    # res = await session.execute(insert(database.AlreadyFoundsLinks), values)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=500, detail="Task failed or result not available"
        )


async def get_founded_links(session: AsyncSession):
    links = list(
        (await session.execute(select(database.AlreadyFoundsLinks))).scalars().all()
    )
    return [link.link for link in links]
