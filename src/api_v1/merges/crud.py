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
    return MergeResult(result="success merge groups", replaced_information="replaced 0")
