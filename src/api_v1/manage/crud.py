from datetime import datetime, timedelta
from typing import List
from sqlalchemy import *
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker
import json

from sqlalchemy.sql.ddl import CreateTable

from src.alchemy import database
from src.api_v1.groups.schemas import Zamena, Paras, DayScheduleFormatted
from src.models.day_schedule_model import DaySchedule, Para
from src.utils.tools import get_number_para_emoji


async def sync_local_database(
    source_session: AsyncSession, target_session: AsyncSession
):
    table_names = ["AlreadyFoundsLinks"]

    for table_name in table_names:
        await copy_table(source_session, target_session, table_name)

    return {"res": "ok"}


async def copy_table(
    source_session: AsyncSession,
    target_session: AsyncSession,
    table_name: str,
    force: bool = True,
):
    # Загружаем метаданные
    metadata = MetaData()

    # Загружаем таблицу из исходной базы данных
    source_table = Table(table_name, metadata, autoload_with=source_session.bind)

    # Проверяем, существует ли таблица в целевой базе данных
    try:
        target_table = Table(table_name, metadata, autoload_with=target_session.bind)
        print(f"Таблица '{table_name}' уже существует в целевой базе данных.")
    except NoSuchTableError:
        if force:
            # Если таблица не существует и force=True, создаем её
            await target_session.execute(CreateTable(source_table))
            print(f"Создана таблица '{table_name}' в целевой базе данных.")
        else:
            print(
                f"Таблица '{table_name}' не найдена и force=False, пропуск копирования."
            )
            return

    # Перенос данных из исходной таблицы в целевую
    select_query = select(source_table)
    results = await source_session.execute(select_query)

    async with target_session.begin():
        async for row in results:
            # Вставляем каждую строку в целевую таблицу
            await target_session.execute(insert(target_table).values(**row))

    print(f"Данные из таблицы '{table_name}' успешно перенесены.")
