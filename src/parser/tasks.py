import asyncio
import datetime
from typing import Any

from celery import Celery

from my_secrets import BACKEND_URL, BROKER_URL
from src.parser import methods
from src.parser.schemas import CheckResult

parser_celery_app = Celery(
    "parser",
    broker=BROKER_URL,
    backend=BACKEND_URL,
)


@parser_celery_app.task
def parse_zamena(url: str, date: datetime.datetime) -> dict:
    return methods.parse_zamena(url, date)


@parser_celery_app.task
def get_latest_zamena_link() -> dict:
    return methods.get_latest_zamena_link()


@parser_celery_app.task
def check_new() -> dict[str, Any]:
    return asyncio.run(methods.check_new())
