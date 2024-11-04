from typing import List, Any

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.alchemy.db_helper import *
from . import crud

from .schemas import ParseZamenaRequest, RemoveZamenaRequest

router = APIRouter(tags=["Parser"])


pass_ = os.environ.get("API_SECRET")


@router.get("/get_latest_zamena_link", response_model=dict)
@cache(300)
async def get_latest_zamena_link() -> dict:
    return await crud.get_latest_zamena_link()


@router.get("/get_founded_links", response_model=List[str])
@cache(300)
async def get_founded_links(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> List[str]:
    return await crud.get_founded_links(session=session)


@router.get("/check_new")
async def check_new() -> dict[str, Any]:
    return await crud.check_new()


@router.post("/parse_zamena", response_model=dict)
async def parse_zamena(
    request: ParseZamenaRequest,
) -> dict:
    return await crud.parse_zamena(request)


@router.options("/containers")
def test():
    return get_containers()


@router.get("/containers")
def get_containers():
    return crud.get_containers()


@router.delete("/zamena")
def delete_zamena(request: RemoveZamenaRequest):
    return crud.delete_zamena(request)
