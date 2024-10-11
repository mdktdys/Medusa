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
import os
import traceback
from io import BytesIO
from typing import List
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


async def check_new() -> CheckResult:
    try:
        html = urlopen(SCHEDULE_URL).read()
        soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
        tables: List[ZamTable] = getAllMonthTables(soup=soup)
        site_links = getAllTablesLinks(tables)
        database_links: List[ParsedDate] = sup.get_zamena_file_links()
        print(f"database_links : {database_links}")
        already_found_links: List[str] = sup.get_already_found_links()
        # await on_check(bot=bot)
        if not site_links.__eq__(database_links):

            # alreadyFound = await r.lrange("alreadyFound", 0, -1)
            new_links = list(
                set(site_links)
                - set([x.link for x in database_links])
                - set(already_found_links)
            )
            new_links.reverse()
            if len(new_links) < 1:
                print("NO NEW")
                print("CHECK EXISTING")
                for i in tables[0].zamenas:
                    if i.date > datetime.date.today():
                        file_bytes = get_remote_file_bytes(link=i.link)
                        file_hash = get_bytes_hash(file_bytes)
                        try:
                            old_hash = [x for x in database_links if x.link == i.link][
                                0
                            ].hash
                            if file_hash != old_hash:
                                file_date = datetime.datetime(
                                    year=i.date.year, month=i.date.month, day=i.date.day
                                )
                                file_stream = BytesIO()
                                file_stream.write(file_bytes)
                                extension = define_file_format(stream=file_stream)

                                screenshots_bytes: List[bytes] = []

                                if extension == "pdf":
                                    screenshots_bytes = create_pdf_screenshots_bytes(
                                        data_bytes=file_bytes
                                    )
                                if extension == "docx":
                                    filename = i.link.split("/")[-1].split(".")[0]
                                    convert(f"{filename}.{extension}")
                                    screenshot_paths = await create_pdf_screenshots(
                                        filename
                                    )
                                    cleanup_temp_files(screenshot_paths)
                                    os.remove(f"{filename}.pdf")
                                sup.table("Zamenas").delete().eq(
                                    "date", file_date
                                ).execute()
                                sup.table("ZamenasFull").delete().eq(
                                    "date", file_date
                                ).execute()
                                res = (
                                    sup.table("ZamenaFileLinks")
                                    .update({"hash": hash})
                                    .eq("link", i.link)
                                    .execute()
                                )
                                parse_zamenas(url=i.link, date_=file_date)
                        except Exception as error:
                            print(error)
                            return {"res": "err", "mes": str(traceback.format_exc())}
                        pass
            else:
                result = CheckResultFoundNew(result="FoundNew")
                # links = [
                #     {
                #         "link": link,
                #     }
                #     for link in new_links
                # ]
                # sup.client.table("AlreadyFoundsLinks").insert(links).execute()
                # return {"res": "add to database"}

                # return {"res": "new_links", "links": new_links}

                for link in new_links:
                    zamena_table = [x for x in tables if x.links.__contains__(link)][0]
                    zamena_cell = [x for x in zamena_table.zamenas if x.link == link][0]
                    try:
                        # await r.lpush("alreadyFound", str(zamm.link))
                        if link.__contains__("google.com") or link.__contains__(
                            "yadi.sk"
                        ):
                            continue

                        file_bytes = get_remote_file_bytes(link=zamena_cell.link)
                        file_hash = get_bytes_hash(file_bytes)
                        file_stream = BytesIO()
                        file_stream.write(file_bytes)
                        extension = define_file_format(stream=file_stream)
                        screenshots_base64: List[str] = []

                        match extension:
                            case "application/pdf":
                                screenshots_base64 = create_pdf_screenshots_bytes(
                                    file_bytes
                                )

                            case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                                raise Exception("invalid format word")
                                # cleanup_temp_files(screenshot_paths)
                                # os.remove(f"{filename}.pdf")
                            case _:
                                raise Exception("invalid format word")

                        result.checks.append(
                            CheckZamenaResultSuccess(
                                date=zamena_cell.date,
                                images=screenshots_base64,
                                link=zamena_cell.link,
                            )
                        )
                        # if extension == "docx":
                        #     filename = zamena_cell.link.split("/")[-1].split(".")[0]
                        #     convert(f"{filename}.{extension}")
                        #     screenshot_paths = await create_pdf_screenshots(filename)

                        # media_group = MediaGroupBuilder(
                        #     caption=f"Новые замены на <a href='{zamm.link}'>{zamm.date}</a>  "
                        # )
                        # for i in screenshot_paths:
                        #     image = FSInputFile(i)
                        #     media_group.add_photo(image)
                        # try:
                        #     # await bot.send_media_group(chat_id=admins[0], media=media_group.build())
                        #     await bot.send_media_group(
                        #         -1002035415883, media=media_group.build()
                        #     )
                        #     send_message_to_topic(
                        #         "Новые замены", f"Новые замены на {zamm.date}", sup=sup
                        #     )
                        # except Exception as error:
                        #     await bot.send_message(chat_id=admins[0], text=str(error))
                        # subs = await r.lrange("subs", 0, -1)
                        # for i in subs:
                        #     try:
                        #         await bot.send_media_group(i, media=media_group.build())
                        #     except Exception as error:
                        #         try:
                        #             await bot.send_message(
                        #                 chat_id=admins[0], text=str(error)
                        #             )
                        #         except:
                        #             continue

                        # datess = datetime.date(
                        #     zamm.date.year, zamm.date.month, zamm.date.day
                        # )
                        # sup.table("Zamenas").delete().eq("date", datess).execute()
                        # sup.table("ZamenasFull").delete().eq("date", datess).execute()
                        # sup.table("ZamenaFileLinks").delete().eq("date", datess).execute()
                        # parse_zamenas(url=zamm.link, date_=datess)
                        # await bot.send_message(chat_id=admins[0], text="parsed")
                    except Exception as e:
                        result.checks.append(
                            CheckZamenaResultFailed(
                                error=str(e),
                                trace=Html.escape(str(traceback.format_exc())),
                            )
                        )
                    pass
                print(result)
                print(result.result)
                print(result.checks)
                print(result.checks[0].result)
                print(result.checks[0].images)
                return result
        return CheckResult(result="Checked")
    except Exception as e:
        return CheckResultError(
            result="Error", trace=Html.escape(str(traceback.format_exc())[0:100]), error=str(e)
        )
