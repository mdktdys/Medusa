import datetime
from io import BytesIO
from typing import Any

import docker
from celery.result import AsyncResult
from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.data_source import DataSource
from src.alchemy import database
from src.api_v1.parser.schemas import ParseZamenaJsonRequest, ParseZamenaRequest, RemoveZamenaRequest
from src.parser import tasks


async def parse_zamena(request: ParseZamenaRequest) -> dict:
    task: AsyncResult = tasks.parse_zamena.delay(
        url = request.url.__str__(),
        date = request.date,
        notify = request.notify
    )
    return task.get()


def parse_zamena_json(request: ParseZamenaJsonRequest) -> dict:
    task: AsyncResult = tasks.parse_zamena_json.delay(
        url = request.file,
        date = request.date,
    )
    return {'task_id': task.id.__str__()}


async def get_latest_zamena_link():
    task: AsyncResult = tasks.get_latest_zamena_link.delay()
    return task.get()


async def check_new() -> dict[str, Any]:
    task: AsyncResult = tasks.check_new.delay()
    return task.get()


async def get_all_tasks() -> dict[str, Any]:
    task: AsyncResult = tasks.get_all_tasks.delay()
    return task.get()


async def delete_zamena(request: RemoveZamenaRequest) -> dict[str, Any]:
    task: AsyncResult = tasks.delete_zamena.delay(date=request.date)
    return task.get()


async def get_founded_links(session: AsyncSession):
    links = list((await session.execute(select(database.AlreadyFoundsLinks))).scalars().all())
    return [link.link for link in links]


async def pdf2docx(docx: UploadFile) -> BytesIO:
    file_bytes = await docx.read()
    from src.parser.parsers import convert_pdf_2_word 
    return convert_pdf_2_word(file=file_bytes)


async def parse_group_schedule_v3(file: UploadFile, monday_date: datetime.date):
    file_bytes = await file.read()
    task: AsyncResult = tasks.parse_group_schedule_v3.delay(file_bytes, monday_date)
    return task.get()


def get_containers():
    client = docker.from_env()
    containers = client.containers.list(all=True)
    container_info = []

    for container in containers:
        container_attrs = container.attrs
        state = container_attrs["State"]

        finished_at = (
            state["FinishedAt"]
            if state["FinishedAt"] != "0001-01-01T00:00:00Z"
            else None
        )

        container_info.append(
            {
                "name": container.name,
                "status": container.status,
                "image": container.image.tags,
                "started_at": state["StartedAt"],
                "finished_at": finished_at,
            }
        )

    return {"containers": container_info}
