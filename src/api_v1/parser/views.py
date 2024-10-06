import datetime
import os
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from src.alchemy.db_helper import *
from . import crud
import docker

from .schemas import ParseZamenaRequest

router = APIRouter(tags=["Parser"])

pass_ = os.environ.get("API_SECRET")


@router.get("/get_latest_zamena_link_celery", response_model=dict)
@cache(300)
async def get_latest_zamena_link_celery() -> dict:
    return await crud.get_latest_zamena_link()


@router.get("/get_founded_links", response_model=List[str])
@cache(300)
async def get_founded_links(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> List[str]:
    return await crud.get_founded_links(session=session)


@router.get("/check_new", response_model=List[str])
async def check_new(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> dict:
    return await crud.check_new(session=session)


@router.post("/parse_zamena", response_model=dict)
async def parse_zamena(
    request: ParseZamenaRequest,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> dict:
    return await crud.parse_zamena(request)


@router.get("/containers")
def get_containers():
    client = docker.from_env()  # Используем Docker SDK для Python
    containers = client.containers.list(all=True)  # Получаем список всех контейнеров
    container_info = []

    for container in containers:
        # Получаем атрибуты контейнера (включает информацию о состоянии)
        container_attrs = container.attrs
        print(container_attrs)
        state = container_attrs["State"]

        # Время завершения контейнера (если остановлен)
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
                "started_at": state["StartedAt"],  # Время запуска контейнера
                "finished_at": finished_at,  # Время завершения работы (если остановлен)
            }
        )

    return container_info
