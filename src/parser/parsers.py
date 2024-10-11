"""
Модуль описывающий работу бота телеграм
"""

import magic
import requests
from io import BytesIO
from http import HTTPStatus
from datetime import date
from pdf2docx import Converter
from src.parser.core import parseParas
from src.parser.models.data_model import Data
from src.parser.supabase import SupaBaseWorker
from src.parser.zamena_parser import parseZamenas


def init_date_model() -> Data:
    data_model = Data
    supabase_client = SupaBaseWorker()

    (
        data_model.GROUPS,
        _,
        data_model.TEACHERS,
        data_model.CABINETS,
        data_model.COURSES,
    ) = supabase_client.get_data_models_list
    return data_model


def get_file_stream(link: str) -> BytesIO:
    response = requests.get(link)

    if response.status_code == HTTPStatus.OK.value:
        stream = BytesIO()
        stream.write(response.content)
    else:
        raise Exception("Данные не получены")
    return stream


def get_remote_file_bytes(link: str) -> bytes:
    response = requests.get(link)
    if response.status_code == HTTPStatus.OK.value:
        return response.content
    else:
        raise Exception("Данные не получены")


def get_file_bytes(link: str) -> bytes:
    response = requests.get(link)

    if response.status_code == HTTPStatus.OK.value:
        return response.content
    else:
        raise Exception("Данные не получены")


def define_file_format(stream: BytesIO):
    data = stream.getvalue()
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(data)

    return file_type


def parse_zamenas(url: str, date_: date):
    supabase_client = SupaBaseWorker()
    data_model = init_date_model()
    stream = get_file_stream(link=url)
    file_type = define_file_format(stream)

    match file_type:
        case "application/pdf":
            cv = Converter(stream=stream, pdf_file="temp")
            stream_converted = BytesIO()
            cv.convert(stream_converted)
            cv.close()

            parseZamenas(stream_converted, date_, data_model, url, supabase_client)
        case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            parseZamenas(stream, date_, data_model, url, supabase_client)


def parse_schedule(url: str, date_: date):
    supabase_client = SupaBaseWorker()
    data_model = init_date_model()
    stream = get_file_stream(link=url)
    file_type = define_file_format(stream)
    bytes = get_file_bytes(link=url)

    # cv = Converter(pdf_file='fixed.pdf')
    # cv.convert(docx_filename=f"schedule {date_}.docx")
    # #cv = Converter(stream=bytes, pdf_file=f'main_schedule {date_}')
    # stream_converted = BytesIO()
    # cv.convert(stream_converted)
    # cv.close()
    # parseParas(date=date_, supabase_worker=supabase_client, data=data_model, stream=stream_converted)
    match file_type:
        case "application/pdf":
            # cv = Converter(pdf_file='fixed.pdf')
            cv = Converter(stream=bytes, pdf_file=f"schedule {date_}")
            stream_converted = BytesIO()
            cv.convert(stream_converted)
            cv.close()

            parseParas(
                date=date_,
                supabase_worker=supabase_client,
                data=data_model,
                stream=stream_converted,
            )
        case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            parseParas(
                date=date_,
                supabase_worker=supabase_client,
                data=data_model,
                stream=stream,
            )
            pass
