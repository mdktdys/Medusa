import datetime

# from broker import parser_celery_ap
import asyncio
import functools

from celery import Celery

from my_secrets import BACKEND_URL, BROKER_URL
from src.parser import methods


# def sync(f):
#     @functools.wraps(f)
#     def wrapper(*args, **kwargs):
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#         return loop.run_until_complete(f(*args, **kwargs))
#
#     return wrapper


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
def get_latest_zamena_link_telegram(chat_id) -> None:
    asyncio.run(methods.get_latest_zamena_link_telegram(chat_id))


@parser_celery_app.task
def check_new() -> dict:
    return methods.check_new()
