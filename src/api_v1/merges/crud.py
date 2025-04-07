from typing import List
from sqlalchemy.engine import Result
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from src.alchemy import database
from src.alchemy.database import Teachers, Cabinets, Loadlinkers
from src.api_v1.cabinets.crud import get_cabinet_by_id
from src.api_v1.cabinets.schemas import Cabinet
from src.api_v1.merges.schemas import MergeResult
from src.api_v1.search.schemas import SearchResult
from src.api_v1.teachers.crud import get_teacher_by_id
from src.api_v1.teachers.schemas import Teacher


async def merge_teachers(
    session: AsyncSession, merge_from_id: int, merge_to_id: int
) -> MergeResult:
    async with session.begin():
        logs = dict()

        query = (
            update(database.Paras)
            .returning(database.Paras.teacher)
            .where(database.Paras.teacher == merge_from_id)
            .values(teacher=merge_to_id)
        )
        result = await session.execute(query)
        logs["paras"] = len(result.fetchall())

        query = (
            update(database.Loadlinkers)
            .returning(database.Loadlinkers.teacher)
            .where(database.Loadlinkers.teacher == merge_from_id)
            .values(teacher=merge_to_id)
        )
        result = await session.execute(query)
        logs["loadlinkers"] = len(result.fetchall())

        query = (
            update(database.Zamenas)
            .returning(database.Zamenas.teacher)
            .where(database.Zamenas.teacher == merge_from_id)
            .values(teacher=merge_to_id)
        )
        result = await session.execute(query)
        logs["zamenas"] = len(result.fetchall())

        teacher_from: Teachers = (await get_teacher_by_id(session=session, teacher_id=merge_from_id))[0]
        teacher_to: Teachers = (await get_teacher_by_id(session=session, teacher_id=merge_to_id))[0]

        teacher_from_synonyms = teacher_from.synonyms
        teacher_to_synonyms = teacher_to.synonyms
        merged_synonyms = teacher_from_synonyms + teacher_to_synonyms
        
        query = (
            update(database.Teachers)
            .returning(database.Teachers.id)
            .where(database.Teachers.id == merge_to_id)
            .values(synonyms=merged_synonyms)
        )
        result = await session.execute(query)
        print(result)
        logs["synonyms"] = merged_synonyms

        query = delete(database.Teachers).where(database.Teachers.id == merge_from_id)
        result = await session.execute(query)
        print(result)

        await session.commit()
    return MergeResult(
        result="success merge teachers",
        replaced_information=f"{logs}",
    )


async def merge_cabinets(
    session: AsyncSession, merge_from_id: int, merge_to_id: int
) -> MergeResult:
    async with session.begin():
        logs = dict()

        # merge paras
        query = (
            update(database.Paras)
            .returning(database.Paras.cabinet)
            .where(database.Paras.cabinet == merge_from_id)
            .values(cabinet=merge_to_id)
        )
        result = await session.execute(query)
        logs["paras"] = len(result.fetchall())

        # merge zamenas
        query = (
            update(database.Zamenas)
            .returning(database.Zamenas.cabinet)
            .where(database.Zamenas.cabinet == merge_from_id)
            .values(cabinet=merge_to_id)
        )
        result = await session.execute(query)
        logs["zamenas"] = len(result.fetchall())

        cabinet_from: Cabinets = (
            await get_cabinet_by_id(session=session, cabinet_id=merge_from_id)
        )[0]
        cabinet_to: Cabinets = (
            await get_cabinet_by_id(session=session, cabinet_id=merge_to_id)
        )[0]

        cabinet_from_synonyms = cabinet_from.synonyms
        cabinet_to_synonyms = cabinet_to.synonyms
        merged_synonyms = cabinet_from_synonyms + cabinet_to_synonyms
        # merge paras
        query = (
            update(database.Cabinets)
            .returning(database.Cabinets.id)
            .where(database.Cabinets.id == merge_to_id)
            .values(synonyms=merged_synonyms)
        )
        result = await session.execute(query)
        print(result)
        logs["synonyms"] = merged_synonyms

        query = delete(database.Cabinets).where(database.Cabinets.id == merge_from_id)
        result = await session.execute(query)
        print(result)

        await session.commit()
    return MergeResult(
        result="success cabinets",
        replaced_information=f"{logs}",
    )


async def merge_groups(
    session: AsyncSession, merge_from_id: int, merge_to_id: int
) -> MergeResult:
    async with session.begin():
        logs = dict()

        # merge liquidation
        query = (
            update(database.Liquidation)
            .returning(database.Liquidation.group)
            .where(database.Liquidation.group == merge_from_id)
            .values(group=merge_to_id)
        )
        result = await session.execute(query)
        logs["liquidation"] = len(result.fetchall())

        # merge practices
        query = (
            update(database.Practices)
            .returning(database.Practices.group)
            .where(database.Practices.group == merge_from_id)
            .values(group=merge_to_id)
        )
        result = await session.execute(query)
        logs["liquidation"] = len(result.fetchall())

        # merge fullzamenas
        query = (
            update(database.ZamenasFull)
            .returning(database.ZamenasFull.group)
            .where(database.ZamenasFull.group == merge_from_id)
            .values(group=merge_to_id)
        )
        result = await session.execute(query)
        logs["zamenasfull"] = len(result.fetchall())

        # merge zamenas
        query = (
            update(database.Zamenas)
            .returning(database.Zamenas.group)
            .where(database.Zamenas.group == merge_from_id)
            .values(group=merge_to_id)
        )
        result = await session.execute(query)
        logs["zamenas"] = len(result.fetchall())

        # merge paras
        query = (
            update(database.Paras)
            .returning(database.Paras.group)
            .where(database.Paras.group == merge_from_id)
            .values(group=merge_to_id)
        )
        result = await session.execute(query)
        logs["paras"] = len(result.fetchall())

        query = delete(database.Groups).where(database.Groups.id == merge_from_id)
        result = await session.execute(query)
        print(result)

        await session.commit()
    return MergeResult(
        result="success merge groups",
        replaced_information=f"{logs}",
    )
