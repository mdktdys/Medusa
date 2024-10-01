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
    # Загружаем метаданные
    metadata = MetaData()

    # Создаем синхронный движок для отражения таблиц
    sync_source_engine = create_engine(source_session.bind.url)
    sync_target_engine = create_engine(target_session.bind.url)

    # Работаем с синхронным движком для загрузки схемы таблицы
    with sync_source_engine.connect() as source_conn:
        metadata.reflect(bind=source_conn)

    source_table = metadata.tables.get(table_name)

    if not source_table:
        raise Exception(f"Table {table_name} not found in source database.")

    # Проверяем, существует ли целевая таблица
    target_metadata = MetaData()

    with sync_target_engine.connect() as target_conn:
        target_metadata.reflect(bind=target_conn)

        target_table = target_metadata.tables.get(table_name)

        if not target_table:
            print(
                f"Table {table_name} does not exist in target_db. Creating the table."
            )
            # Создаем таблицу, если она не существует
            target_metadata.create_all(bind=target_conn, tables=[source_table])

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
