from fastapi import UploadFile
import magic
from pydantic_core import Url
import requests
from io import BytesIO
from http import HTTPStatus
from datetime import date
from pdf2docx import Converter

from src.dependencies.data_source_dependency import get_supabase_data_source
from src.data.data_source import DataSource
from src.api_v1.telegram.views import notify_zamena
from src.parser.core import parseParas
from src.parser.models.data_model import Data
from src.parser.schemas.parse_zamena_schemas import ZamenaParseResult, ZamenaParseSucess
from src.parser.supabase import SupaBaseWorker
from src.parser.zamena_parser import parseZamenas, parse_zamena_v2


def init_date_model(sup: SupaBaseWorker) -> Data:
    return Data(sup=sup)


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


def convert_pdf2word(url: str, file_name: str):
    stream: BytesIO = get_file_stream(link=url)
    cv = Converter(stream=stream, pdf_file="temp")
    cv.convert(docx_filename=file_name)
    cv.close()


def convert_pdf_2_word(file: bytes) -> BytesIO:
    stream_converted = BytesIO()

    cv = Converter(stream=file, pdf_file="temp")
    cv.convert(stream_converted)
    cv.close()
    return stream_converted


async def parse_zamenas_from_word(file_bytes: BytesIO, date_: date, force: bool, url: str):
    supabase_client = SupaBaseWorker()
    data_model = init_date_model(sup=supabase_client)
    return parseZamenas(file_bytes, date_, data_model, url, supabase_client, force=force)


async def parse_zamenas_json(url: str | UploadFile, date: date) -> dict:
    supabase_client = SupaBaseWorker()
    data_model = init_date_model(sup=supabase_client)
    
    stream = None
    if type(url) is str:
        stream = get_file_stream(link=url.__str__())
    if type(url) is UploadFile:
        stream = url.file.read()
        
        
    file_type: str = define_file_format(stream)
    match file_type:
        case "application/pdf":
            raise Exception('Пока не поддерживается')
        case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            result: ZamenaParseResult = parse_zamena_v2(
                supabase_client = supabase_client,
                data_model = data_model,
                stream = stream,
                date = date,
                link = url,
            )
        case _:
            raise Exception('Неизвестный формат')

    return {
        'result': result.model_dump(),
        'test': 'test'
    }


async def parse_zamenas(url: str, date_: date, force: bool, notify: bool) -> ZamenaParseResult:
    supabase_client = SupaBaseWorker()
    data_model: Data = init_date_model(sup=supabase_client)
    stream: BytesIO = get_file_stream(link=url)
    file_type: str = define_file_format(stream)
    result: ZamenaParseResult

    match file_type:
        case "application/pdf":
            cv = Converter(stream=stream, pdf_file="temp")
            stream_converted = BytesIO()
            cv.convert(stream_converted)
            cv.close()

            result = parseZamenas(stream_converted, date_, data_model, url, supabase_client, force=force)
        case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            result = parseZamenas(stream, date_, data_model, url, supabase_client, force=force)
        case _:
            raise Exception('Неизвестный формат')

    if notify and type(result) is ZamenaParseSucess:
        await notify_zamena(
            affected_groups = result.affected_groups,
            affected_teachers = result.affected_teachers
        )

    return result


def parse_schedule(url: str, date_: date):
    supabase_client = SupaBaseWorker()
    data_model = init_date_model(sup=supabase_client)
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
