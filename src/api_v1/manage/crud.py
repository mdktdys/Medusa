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

from my_secrets import supabase_database_connection, local_database_connection
from src.alchemy import database
from src.api_v1.groups.schemas import Zamena, Paras, DayScheduleFormatted
from src.models.day_schedule_model import DaySchedule, Para
from src.utils.tools import get_number_para_emoji


async def sync_local_database(
    source_session: AsyncSession, target_session: AsyncSession
):
    table_names = [
        "AlreadyFoundsLinks",
        "Cabinets",
        "Courses",
        "Departments",
        "Groups",
        "Holidays",
        "Liquidation",
        "MessagingClients",
        "Paras",
        "Practices",
        "Subscribers",
        "Teachers",
        "ZamenaFileLinks",
        "Zamenas",
        "ZamenasFull",
        "scheduleTimetable",
        "timings",
    ]
    await copy_tables(
        table_names=table_names,
        source_session=source_session,
        target_session=target_session,
        force=True,
    )

    return {"res": "ok"}


async def copy_tables(
    table_names: List[str],
    source_session: AsyncSession,
    target_session: AsyncSession,
    force: bool = True,
):
    src_engine = create_engine(supabase_database_connection.replace("+asyncpg", ""))
    src_metadata = MetaData()

    tgt_engine = create_engine(local_database_connection.replace("+asyncpg", ""))
    tgt_metadata = MetaData()

    src_conn = src_engine.connect()
    tgt_conn = tgt_engine.connect()
    tgt_metadata.reflect(bind=tgt_engine)

    # Если force=True, удаляем все строки из таблиц в целевой базе данных
    for table in tgt_metadata.sorted_tables:
        if table.name in table_names:
            print(f"Очистка таблицы {table.name}")
            tgt_conn.execute(table.delete())  # Удаляем все строки из таблицы

    tgt_conn.commit()  # Сохраняем изменения после очистки таблиц

    # Отражаем (рефлексируем) метаданные заново после очистки
    tgt_metadata.clear()
    tgt_metadata.reflect(bind=tgt_engine)
    src_metadata.reflect(bind=src_engine)

    # Копируем структуру таблиц из исходной базы данных в целевую, если их еще нет
    for table in src_metadata.sorted_tables:
        if table.name in table_names and table.name not in tgt_metadata.tables:
            table.create(bind=tgt_engine)

    # Копируем данные из исходной базы данных в целевую
    for table in src_metadata.sorted_tables:
        if table.name in table_names:
            src_table = src_metadata.tables[table.name]
            stmt = table.insert()  # Подготавливаем вставку данных
            for index, row in enumerate(src_conn.execute(src_table.select())):
                print(f"Таблица {table.name}: Вставка строки {index}")
                tgt_conn.execute(stmt.values(row))

    tgt_conn.commit()  # Сохраняем все изменения после копирования данных
    src_conn.close()
    tgt_conn.close()
