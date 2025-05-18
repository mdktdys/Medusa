import asyncio
import datetime
from io import BytesIO
from typing import Any

from celery import Celery
from celery.app.control import Inspect

from my_secrets import BACKEND_URL, BROKER_URL
from src.parser.schemas.parse_zamena_schemas import ZamenaParseResultJson
from src.parser import methods

parser_celery_app = Celery(
    "parser",
    backend=BACKEND_URL,
    broker=BROKER_URL,
)


@parser_celery_app.task
def parse_zamena(url: str, date: datetime.datetime, notify: bool) -> dict:
    return asyncio.run(methods.parse_zamena(url, date, notify))

@parser_celery_app.task
def parse_zamena_json(url: str, date: datetime.date) -> dict:
    
    return {
        'result': 'gotcha'
    }

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


@parser_celery_app.task
def get_all_tasks() -> dict:
    temp: Inspect = parser_celery_app.control.inspect()
    tasks = temp.registered_tasks
    
    if tasks is dict:
        return tasks # type: ignore
    else:
        return {'result': f'no ok {type(tasks())} {tasks}'}
