import asyncio
import datetime
from functools import wraps
from io import BytesIO
from typing import Any

from celery import Celery, Task
from fastapi import UploadFile
from pdf2docx import Converter

import src.parser.zamena.zamena_v3_parser as zamena_parser
from my_secrets import BACKEND_URL, BROKER_URL
from src.alchemy.db_helper import local_db_helper
from src.parser import methods
from src.parser.schemas.parse_zamena_schemas import ZamenaParseResult
from src.utils.define_file_format import define_file_format_from_bytes, is_pdf, is_word
from src.utils.telegram_sender import send_telegram_message

parser_celery_app = Celery(
    "parser",
    backend=BACKEND_URL,
    broker=BROKER_URL,
)


class BaseTaskWithAlert(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        msg = (
            f"❌ Ошибка в задаче!\n\n"
            f"Task: {self.name}\n"
            f"ID: {task_id}\n"
            f"Args: {args}\n"
            f"Kwargs: {kwargs}\n"
            f"Exception: {exc}\n"
        )
        send_telegram_message(msg)


def with_session(func):
    @wraps(func)
    def _sync_wrapper(*args, **kwargs):
        async def _inner():
            # local_db_helper._ensure_initialized()  # ← убрать
            async with local_db_helper.session_factory() as session:
                kwargs_with_session = {**kwargs, "session": session}
                return await func(*args, **kwargs_with_session)
        return asyncio.run(_inner())
    return _sync_wrapper


@parser_celery_app.task
def parse_zamena(url: str, date: datetime.datetime, notify: bool) -> dict:
    return asyncio.run(methods.parse_zamena(url, date, notify))

@parser_celery_app.task
def parse_zamena_json(url: str | UploadFile, date: datetime.date) -> ZamenaParseResult:
    pass
    # return asyncio.run(methods.parse_zamenas_json(url = url, date = date))

@parser_celery_app.task
def get_latest_zamena_link() -> dict:
    return methods.get_latest_zamena_link()

@parser_celery_app.task
def check_new() -> dict[str, Any]:
    return asyncio.run(methods.check_new())

@parser_celery_app.task
def delete_zamena(date: datetime.date) -> dict[str, Any]:
    return asyncio.run(methods.delete_zamena(date=date))

@parser_celery_app.task
def parse_group_schedule_v3(file: BytesIO, monday_date: datetime.date) -> dict:
    return asyncio.run(methods.parse_group_schedule_v3(file, monday_date))


@parser_celery_app.task(base = BaseTaskWithAlert)
@with_session
async def parse_zamena_v3(bytes_: bytes, session):
    file_format: str = define_file_format_from_bytes(bytes_ = bytes_)
    stream: BytesIO = BytesIO()

    if is_pdf(file_format):
        cv = Converter(stream=bytes_, pdf_file="temp")
        cv.convert(stream)
        cv.close()
    
    if is_word(file_format):
        stream = BytesIO(bytes_)

    return await zamena_parser.parse_zamena_v3(
        stream = stream,
        session = session,
    )