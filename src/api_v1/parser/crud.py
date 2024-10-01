import asyncio
from typing import List

from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from fastapicelery import fastapi_celery_app
from src.alchemy import database


async def get_latest_zamena_link():
    # Отправляем задачу в Celery
    task = fastapi_celery_app.send_task("parser.tasks.get_latest_zamena_link")

    # Используем asyncio для асинхронного ожидания результата
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
    result: list = await asyncio.to_thread(task.get, timeout=60)

    values = [{"link": link} for link in result]

    res = await session.execute(insert(database.AlreadyFoundsLinks), values)
    print(res)
    return "ok"

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
