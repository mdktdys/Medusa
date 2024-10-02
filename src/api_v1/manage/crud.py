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
    src_engine = create_engine(source_session.bind.url)
    src_metadata = MetaData()

    tgt_engine = create_engine(target_session.bind.url)
    tgt_metadata = MetaData()

    src_conn = src_engine.connect()
    tgt_conn = tgt_engine.connect()
    tgt_metadata.reflect(bind=tgt_engine)

    for table in reversed(tgt_metadata.sorted_tables):
        if table.name in table_names:
            print("dropping table =", table.name)
            table.drop(bind=tgt_engine)

    tgt_metadata.clear()
    tgt_metadata.reflect(bind=tgt_engine)
    src_metadata.reflect(bind=src_engine)

    # create all tables in target database
    for table in src_metadata.sorted_tables:
        if table.name in table_names:
            table.create(bind=tgt_engine)

    # refresh metadata before you can copy data
    tgt_metadata.clear()
    tgt_metadata.reflect(bind=tgt_engine)

    # Copy all data from src to target
    for table in tgt_metadata.sorted_tables:
        src_table = src_metadata.tables[table.name]
        stmt = table.insert()
        for index, row in enumerate(src_conn.execute(src_table.select())):
            print("table =", table.name, "Inserting row", index)
            tgt_conn.execute(stmt.values(row))

    tgt_conn.commit()
    src_conn.close()
    tgt_conn.close()
