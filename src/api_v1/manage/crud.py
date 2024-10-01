from datetime import datetime, timedelta
from typing import List
from sqlalchemy import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker
import json
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
    # Загружаем метаданные и таблицу из исходной базы данных
    metadata = MetaData()
    source_table = Table(table_name, metadata, autoload_with=source_session.bind)

    # Загружаем метаданные целевой базы данных
    target_metadata = MetaData()

    # Попытаемся отразить таблицу из целевой базы данных
    try:
        target_table = Table(
            table_name, target_metadata, autoload_with=target_session.bind
        )
    except Exception as e:
        print(f"Table {table_name} does not exist in target_db. Creating the table.")

        # Создаем таблицу, если она не существует
        target_table = Table(table_name, target_metadata)
        source_table.metadata.reflect(
            bind=source_session.bind
        )  # Отражаем исходную схему
        source_table.metadata.create_all(
            bind=target_session.bind, tables=[source_table]
        )

    if force:
        # Очистка таблицы в целевой базе данных
        await target_session.execute(target_table.delete())
        await target_session.commit()
        print(f"Table {table_name} in target_db cleared.")

    # Извлекаем все записи из таблицы в исходной базе данных
    result = await source_session.execute(select(source_table))
    rows = result.fetchall()

    # Вставляем данные в целевую таблицу
    if rows:
        for row in rows:
            row_dict = dict(row)  # Преобразуем строку в словарь для вставки
            await target_session.execute(target_table.insert().values(**row_dict))

        # Фиксируем изменения в целевой базе данных
        await target_session.commit()

    print(f"Copied table {table_name} with {len(rows)} rows.")
