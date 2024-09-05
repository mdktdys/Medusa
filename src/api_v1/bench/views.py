import functools
from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
import time
import asyncio
from src.alchemy.db_helper import *
from . import crud
from .schemas import Teacher

router = APIRouter(tags=["Bench"])
# test 2


@router.get("/bench/alchemy/")
async def bench_alchemy(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> List[Teacher]:
    start_time = time.perf_counter()
    res = await crud.bench_alchemy(session=session)
    end_time = time.perf_counter()
    print(f"Время выполнения {end_time - start_time} секунд")
    return res


@router.get("/bench/supabase/")
async def bench_supabase(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> List[Teacher]:
    import os
    from supabase import create_client, Client

    url: str = "https://ojbsikxdqcbuvamygezd.supabase.co"
    key: str = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9qYnNpa3hkcWNidXZhbXlnZXpkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDk0NTM4NDQsImV4cCI6MjAyNTAyOTg0NH0.aAHqihRJKwRlkGpCL2dqVVWoafsWvBWizaPSckZsjm4"
    )
    supabase: Client = create_client(url, key)
    start_time = time.perf_counter()
    res = await crud.bench_supabase(session=session, supabase=supabase)
    end_time = time.perf_counter()
    print(f"Время выполнения {end_time - start_time} секунд")
    return res
