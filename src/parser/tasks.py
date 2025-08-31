import asyncio
import datetime
from io import BytesIO
from typing import Any

from celery import Celery
from fastapi import UploadFile
from pdf2docx import Converter

import src.parser.zamena.zamena_v3_parser as zamena_parser
from my_secrets import BACKEND_URL, BROKER_URL
from src.parser import methods
from src.parser.schemas.parse_zamena_schemas import ZamenaParseResult

parser_celery_app = Celery(
    "parser",
    backend=BACKEND_URL,
    broker=BROKER_URL,
)

@parser_celery_app.task
def parse_zamena(url: str, date: datetime.datetime, notify: bool) -> dict:
    return asyncio.run(methods.parse_zamena(url, date, notify))

@parser_celery_app.task
def parse_zamena_json(url: str | UploadFile, date: datetime.date) -> ZamenaParseResult:
    return asyncio.run(methods.parse_zamenas_json(url = url, date = date))

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
def parse_zamena_v3(bytes_: bytes):
    # check if file is pdf
    
    stream : BytesIO = BytesIO()
    if True:
        cv = Converter(stream = bytes_, pdf_file="temp")
        cv.convert(stream)
        cv.close()
        
    return asyncio.run(zamena_parser.parse_zamena_v3(stream = stream))