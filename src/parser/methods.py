# import asyncio
# import datetime
# from urllib.request import urlopen
# from bs4 import BeautifulSoup
# from typing import List
# from aiogram.fsm.storage import redis
#
# # from celery import signature
# # from celery.result import AsyncResult
#
# from bot_worker import parse_zamenas
# from bot_worker.bot import admins
# from broker import rabbitmq_channel
#
# # from broker import sup, parser_celery_app
# from parser_secrets import (
#     DEBUG_CHANNEL,
#     REDIS_HOST_URL,
#     REDIS_PORT,
#     REDIS_PASSWORD,
#     REDIS_USERNAME,
#     SCHEDULE_URL,
# )
# from src.code.core.schedule_parser import (
#     getLastZamenaLink,
#     getAllMonthTables,
#     getAllTablesLinks,
# )
# from src.code.models.parsed_date_model import ParsedDate
# from src.code.models.zamena_table_model import ZamTable
#
#
# # Функция для отправки сообщений в очередь
# def send_message_to_rabbitmq(message: str) -> None:
#     print(rabbitmq_channel)
#     if rabbitmq_channel is None:
#         print("RabbitMQ channel is not initialized")
#         raise Exception("RabbitMQ channel is not initialized")
#
#     rabbitmq_channel.basic_publish(exchange="", routing_key="parser", body=message)
#     print(f" [x] Sent '{message}' to queue 'parser'")
import datetime
import json
import os
import traceback
from io import BytesIO
from typing import List, Any
from urllib.request import urlopen

from bs4 import BeautifulSoup
from docx2pdf import convert
from my_secrets import SCHEDULE_URL
from src.parser.core import getLastZamenaLink, getAllMonthTables, getAllTablesLinks
from src.parser.models.parsed_date_model import ParsedDate
from src.parser.models.zamena_table_model import ZamTable
from src.parser.parsers import (
    parse_zamenas,
    get_file_bytes,
    define_file_format,
    get_file_stream,
    get_remote_file_bytes,
)
from src.parser.schemas import (
    CheckResult,
    CheckResultError,
    CheckResultFoundNew,
    CheckZamenaResultFailed,
    CheckZamenaResultSuccess,
    CheckResultCheckExisting,
    CheckZamenaResultHashChanged,
    CheckZamenaResultInvalidFormat,
)
import base64
from src.parser.supabase import SupaBaseWorker
from src.parser.zamena_parser import (
    get_remote_file_hash,
    get_file_extension,
    download_file,
    create_pdf_screenshots,
    cleanup_temp_files,
    get_bytes_hash,
    create_pdf_screenshots_bytes,
    create_word_screenshots_bytes,
)
import html as Html

sup = SupaBaseWorker()
# async def send_task(celery_app, task_name: str, args: list = list) -> AsyncResult:
#     max_retries = 5
#     retries = 0
#     while retries < max_retries:
#         task = celery_app.send_task(task_name, args=args)
#         task_id = task.id
#         result = AsyncResult(task_id)
#
#         while not result.ready():
#             await asyncio.sleep(1)
#
#         if result.successful():
#             return result
#         elif result.failed():
#             retries += 1
#             if retries == max_retries:
#                 raise Exception("Достигнут лимит попыток. Попробуйте позже.")
#         raise Exception("Хз что произошло")


def parse_zamena(url: str, date: datetime.datetime):
    try:
        parse_zamenas(url=url, date_=date)
        return {"res": "ok"}
    except Exception as e:
        return {"res": f"{str(e)}"}


def get_latest_zamena_link():
    try:
        html = urlopen("https://www.uksivt.ru/zameny").read()
        soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
        link, date = getLastZamenaLink(soup=soup)
        return {"date": date, "link": link}
    except Exception as e:
        return {"message": "failed", "reason": str(e)}


async def check_new() -> dict[str, Any]:
    try:
        html = urlopen(SCHEDULE_URL).read()
        soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
        tables: List[ZamTable] = getAllMonthTables(soup=soup)
        site_links = getAllTablesLinks(tables)
        database_links: List[ParsedDate] = sup.get_zamena_file_links()
        already_found_links: List[str] = sup.get_already_found_links()
        if not site_links.__eq__(database_links):
            print("not equal links")
            new_links = list(
                set(site_links)
                - set([x.link for x in database_links])
                - set(already_found_links)
            )
            print(len(new_links))
            print(new_links)
            new_links.reverse()
            if len(new_links) < 1:
                result = CheckResultCheckExisting()
                for zamena in tables[0].zamenas:
                    if zamena.date > datetime.date.today():
                        file_bytes = get_remote_file_bytes(link=zamena.link)
                        file_hash = get_bytes_hash(file_bytes)
                        try:
                            old_hash = [
                                x for x in database_links if x.link == zamena.link
                            ]
                            if len(old_hash) == 0:
                                result.checks.append(
                                    CheckZamenaResultFailed(
                                        error="Не смог проверить хеш замены",
                                        trace=f"возможно распес нет парсинга\n{zamena.link}\n{zamena.date}",
                                    )
                                )
                                continue
                            old_hash = old_hash[0].hash
                            if file_hash != old_hash:
                                extension = get_file_extension(zamena.link)
                                filename = zamena.link.split("/")[-1].split(".")[0]
                                download_file(
                                    link=zamena.link, filename=f"{filename}.{extension}"
                                )
                                match extension:
                                    case "pdf":
                                        screenshot_paths = create_pdf_screenshots_bytes(
                                            filename
                                        )
                                    case "docx":
                                        convert(f"{filename}.{extension}")
                                        screenshot_paths = create_pdf_screenshots_bytes(
                                            filename
                                        )
                                    case _:
                                        raise Exception("invalid format word")
                                result.checks.append(
                                    CheckZamenaResultSuccess(
                                        date=zamena.date,
                                        images=screenshot_paths,
                                        link=zamena.link,
                                    )
                                )
                                os.remove(f"{filename}.pdf")
                                date = datetime.datetime(
                                    year=zamena.date.year,
                                    month=zamena.date.month,
                                    day=zamena.date.day,
                                ).strftime("%Y-%m-%d")

                                sup.add_already_found_link(link=zamena.link, date=date)

                                result.checks.append(
                                    CheckZamenaResultHashChanged(
                                        date=zamena.date,
                                        images=screenshot_paths,
                                        link=zamena.link,
                                    )
                                )
                                # sup.table("Zamenas").delete().eq(
                                #     "date", file_date
                                # ).execute()
                                # sup.table("ZamenasFull").delete().eq(
                                #     "date", file_date
                                # ).execute()
                                # res = (
                                #     sup.table("ZamenaFileLinks")
                                #     .update({"hash": hash})
                                #     .eq("link", i.link)
                                #     .execute()
                                # )
                                # parse_zamenas(url=i.link, date_=file_date)
                        except Exception as e:
                            print(e)
                            return CheckResultError(
                                result="Error",
                                trace=Html.escape(str(traceback.format_exc())[0:100]),
                                error=Html.escape(str(e)),
                            ).model_dump()
                return result.model_dump()
            else:
                result = CheckResultFoundNew()
                for link in new_links:
                    zamena_table = [x for x in tables if x.links.__contains__(link)][0]
                    zamena_cell = [x for x in zamena_table.zamenas if x.link == link][0]
                    try:
                        if link.__contains__("google.com") or link.__contains__(
                            "yadi.sk"
                        ):
                            continue
                        extension = get_file_extension(zamena_cell.link)
                        filename = zamena_cell.link.split("/")[-1].split(".")[0]
                        download_file(
                            link=zamena_cell.link, filename=f"{filename}.{extension}"
                        )
                        print(extension)
                        match extension:
                            case "pdf":
                                screenshot_paths = create_pdf_screenshots_bytes(
                                    f"{filename}.{extension}"
                                )
                            # case "docx":
                            # convert(f"{filename}.{extension}")
                            # print(filename)
                            # print(f"{filename}.{extension}")
                            # screenshot_paths = create_word_screenshots_bytes(
                            #     f"{filename}.{extension}"
                            # )

                            case "jpeg":
                                with open(
                                    f"{filename}.{extension}", "rb"
                                ) as image_file:
                                    data = base64.b64encode(image_file.read())
                                    screenshot_paths = [data]
                            case _:
                                result.checks.append(
                                    CheckZamenaResultInvalidFormat(
                                        date=zamena_cell.date,
                                        file=zamena_cell.link,
                                        link=zamena_cell.link,
                                    )
                                )
                                date = datetime.datetime(
                                    year=zamena_cell.date.year,
                                    month=zamena_cell.date.month,
                                    day=zamena_cell.date.day,
                                ).strftime("%Y-%m-%d")
                                sup.add_already_found_link(link=link, date=date)
                                continue
                        result.checks.append(
                            CheckZamenaResultSuccess(
                                date=zamena_cell.date,
                                images=screenshot_paths,
                                link=zamena_cell.link,
                            )
                        )
                        date = datetime.datetime(
                            year=zamena_cell.date.year,
                            month=zamena_cell.date.month,
                            day=zamena_cell.date.day,
                        ).strftime("%Y-%m-%d")
                        print(date)
                        sup.add_already_found_link(link=link, date=date)
                        os.remove(f"{filename}.{extension}")
                    # sup.table("Zamenas").delete().eq("date", datess).execute()
                    # sup.table("ZamenasFull").delete().eq("date", datess).execute()
                    # sup.table("ZamenaFileLinks").delete().eq("date", datess).execute()
                    # parse_zamenas(url=zamm.link, date_=datess)
                    except Exception as e:
                        result.checks.append(
                            CheckZamenaResultFailed(
                                error=str(e),
                                trace=Html.escape(str(traceback.format_exc())[0:200]),
                            )
                        )
                return result.model_dump()
        else:

            return CheckResult(result="Checked").model_dump()
    except Exception as e:
        print(e)
        return CheckResultError(
            result="Error",
            trace=Html.escape(str(traceback.format_exc())[0:100]),
            error=Html.escape(str(e)),
        ).model_dump()
