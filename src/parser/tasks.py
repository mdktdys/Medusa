import asyncio
import datetime
from io import BytesIO
from typing import Any

from celery import Celery

from my_secrets import BACKEND_URL, BROKER_URL
from src.parser import methods

parser_celery_app = Celery(
    "parser",
    broker=BROKER_URL,
    backend=BACKEND_URL,
)


@parser_celery_app.task
def parse_zamena(url: str, date: datetime.datetime) -> dict:
    return asyncio.run(methods.parse_zamena(url, date))


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
def parse_group_schedule_v3(file: BytesIO, monday_date: datetime.date):
    return asyncio.run(methods.parse_group_schedule_v3(file, monday_date))
    
