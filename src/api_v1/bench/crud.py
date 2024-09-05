from datetime import datetime, timedelta
from typing import List
from sqlalchemy import *
from sqlalchemy.ext.asyncio import AsyncSession
from src.alchemy import database
from src.api_v1.bench.schemas import Teacher


async def bench_alchemy(session: AsyncSession) -> List[Teacher]:
    query = select(database.Teachers)
    result: Result = await session.execute(query)
    return list(result.scalars().all())


async def bench_supabase(session: AsyncSession, supabase) -> List[Teacher]:
    data, _ = supabase.table("Teachers").select("*").execute()
    return [Teacher.parse_obj(x) for x in data[1]]
