from typing import List
from sqlalchemy.engine import Result
from sqlalchemy import select, update, delete
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


# @dp.message(F.text, Command("merge_teacher"))
# async def my_handler(message: Message):
#     if message.chat.id in admins:
#         merge_from = message.text.split()[1]
#         merge_to = message.text.split()[2]
#         data = sup.table('Paras').update({'teacher': merge_to}).eq('teacher', merge_from).execute()
#         print(data)
#         count = len(data.data)
#         data = sup.table('Zamenas').update({'teacher': merge_to}).eq('teacher', merge_from).execute()
#         print(data)
#         count = count + len(data.data)
#         sup.table('Teachers').delete().eq('id', merge_from).execute()
#         await message.answer(f"Поменял с {merge_from} на {merge_to} | {count} раз")


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

        print("l")

        # merge practices
        query = (
            update(database.Practices)
            .returning(database.Practices.group)
            .where(database.Practices.group == merge_from_id)
            .values(group=merge_to_id)
        )
        result = await session.execute(query)
        logs["liquidation"] = len(result.fetchall())

        print("p")

        # merge fullzamenas
        query = (
            update(database.ZamenasFull)
            .returning(database.ZamenasFull.group)
            .where(database.ZamenasFull.group == merge_from_id)
            .values(group=merge_to_id)
        )
        result = await session.execute(query)
        logs["zamenasfull"] = len(result.fetchall())

        print("f")

        # merge zamenas
        query = (
            update(database.Zamenas)
            .returning(database.Zamenas.group)
            .where(database.Zamenas.group == merge_from_id)
            .values(group=merge_to_id)
        )
        result = await session.execute(query)
        logs["zamenas"] = len(result.fetchall())

        print("z")

        # merge paras
        query = (
            update(database.Paras)
            .returning(database.Paras.group)
            .where(database.Paras.group == merge_from_id)
            .values(group=merge_to_id)
        )
        result = await session.execute(query)
        logs["paras"] = len(result.fetchall())

        print("p")

        query = delete(database.Groups).where(database.Groups.id == merge_from_id)
        result = await session.execute(query)
        print(result)

        print("d")

        await session.commit()
    return MergeResult(
        result="success merge groups",
        replaced_information=f"{logs}",
    )
