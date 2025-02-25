import os
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from src.alchemy.db_helper import *
from . import crud
import docker

from ...auth.auth import fastapi_users
from ...auth.schemas import User

router = APIRouter(tags=["Manage"])


@router.get("/sync_local_database", response_model=dict)
async def sync_local_database(
    supabase_session: AsyncSession = Depends(db_helper.session_dependency),
    local_session: AsyncSession = Depends(local_db_helper.session_dependency),
) -> dict:
    return await crud.sync_local_database(supabase_session, local_session)

@router.get('/tasks', response_model=dict)
async def get_all_tasks(

) -> dict: