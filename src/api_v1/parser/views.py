import os
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from src.alchemy.db_helper import *
from . import crud
import docker

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


@router.get("/containers")
def get_containers():
    client = docker.from_env()  # Используем Docker SDK для Python
    containers = client.containers.list(all=True)  # Получаем список всех контейнеров
    container_info = []
    for container in containers:
        container_info.append(
            {
                "name": container.name,
                "status": container.status,
                "image": container.image.tags,
            }
        )
    return container_info
