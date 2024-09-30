import os
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from src.alchemy.db_helper import *
from . import crud

router = APIRouter(tags=["Parser"])

pass_ = os.environ.get("API_SECRET")


@router.get("/get_latest_zamena_link_celery", response_model=dict)
@cache(6000)
async def get_latest_zamena_link_celery() -> dict:
    return await crud.get_latest_zamena_link()
