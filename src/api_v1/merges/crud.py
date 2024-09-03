from typing import List
from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from src.alchemy import database
from src.api_v1.merges.schemas import MergeResult
from src.api_v1.search.schemas import SearchResult


async def merge_teachers(
    session: AsyncSession, merge_from_id: int, merge_to_id: int
) -> MergeResult:
    return MergeResult(
        result="success merge teachers", replaced_information="replaced 0"
    )


async def merge_cabinets(
    session: AsyncSession, merge_from_id: int, merge_to_id: int
) -> MergeResult:
    return MergeResult(
        result="success merge cabinets", replaced_information="replaced 0"
    )


async def merge_groups(
    session: AsyncSession, merge_from_id: int, merge_to_id: int
) -> MergeResult:
    return MergeResult(result="success merge groups", replaced_information="replaced 0")
