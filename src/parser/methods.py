import datetime
import os
import traceback
from typing import List, Any
from urllib.request import urlopen

from bs4 import BeautifulSoup
from docx2pdf import convert
from my_secrets import SCHEDULE_URL
from src.parser.core import (
    getLastZamenaLink,
    getAllMonthTables,
    getAllTablesLinks,
    get_all_tables_zamenas,
)
from src.parser.models.parsed_date_model import ParsedDate
from src.parser.models.zamena_table_model import ZamTable
from src.parser.parsers import (
    parse_zamenas,
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
    CheckZamenaResultFailedDownload,
)
import base64
from src.parser.supabase import SupaBaseWorker
from src.parser.zamena_parser import (
    get_remote_file_hash,
    get_file_extension,
    download_file,
    get_bytes_hash,
    create_pdf_screenshots_bytes,
)
import html as Html
from src.parser.models.zamena_model import Zamena

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
        soup = BeautifulSoup(urlopen(SCHEDULE_URL).read(), "html.parser")
        tables = getAllMonthTables(soup=soup)
        site_links = get_all_tables_zamenas(tables)
        database_links = sup.get_zamena_file_links()
        already_found_links = sup.get_already_found_links()
        if not [link.link for link in site_links] == [
            link.link for link in already_found_links
        ]:
            new_links = list(
                set(site_links)
                - set([x.link for x in database_links])
                - set([x.link for x in already_found_links])
            )
            print("not equal links")
            print(len(new_links))
            print(new_links)
            new_links.reverse()
            result = CheckResultFoundNew()
            for link in new_links:
                zamena_table = [x for x in tables if x.links.__contains__(link)][0]
                zamena_cell = [x for x in zamena_table.zamenas if x.link == link][0]
                date = datetime.datetime(
                    year=zamena_cell.date.year,
                    month=zamena_cell.date.month,
                    day=zamena_cell.date.day,
                ).strftime("%Y-%m-%d")
                try:
                    if link.__contains__("google.com") or link.__contains__("yadi.sk"):
                        result.checks.append(
                            CheckZamenaResultFailedDownload(
                                date=zamena_cell.date,
                                link=zamena_cell.link,
                            )
                        )
                        sup.add_already_found_link(link=link, date=date, hash=None)
                        continue
                    extension = get_file_extension(zamena_cell.link)
                    filename = zamena_cell.link.split("/")[-1].replace(
                        f".{extension}", ""
                    )
                    file_downloaded = download_file(
                        link=zamena_cell.link, filename=f"{filename}.{extension}"
                    )
                    if not file_downloaded:
                        print("Fail to download")
                        print(extension)
                        print(filename)
                        print(zamena_cell.link)
                        result.checks.append(
                            CheckZamenaResultFailedDownload(
                                date=zamena_cell.date,
                                link=zamena_cell.link,
                            )
                        )
                        sup.add_already_found_link(link=link, date=date, hash=None)
                        continue

                    file_hash = get_remote_file_hash(url=zamena_cell.link)
                    match extension:
                        case "pdf":
                            screenshot_paths = create_pdf_screenshots_bytes(filename)
                        # case "docx":
                        # convert(f"{filename}.{extension}")
                        # print(filename)
                        # print(f"{filename}.{extension}")
                        # screenshot_paths = create_word_screenshots_bytes(
                        #     f"{filename}.{extension}"
                        # )

                        case "jpeg":
                            with open(f"{filename}.{extension}", "rb") as image_file:
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
                            sup.add_already_found_link(
                                link=link, date=date, hash=file_hash
                            )
                            continue
                    result.checks.append(
                        CheckZamenaResultSuccess(
                            date=zamena_cell.date,
                            images=screenshot_paths,
                            link=zamena_cell.link,
                        )
                    )
                    sup.add_already_found_link(link=link, date=date, hash=file_hash)
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
            result = CheckResultCheckExisting()
            for zamena in tables[0].zamenas:
                if zamena.date > datetime.date.today():
                    file_bytes = get_remote_file_bytes(link=zamena.link)
                    file_hash = get_bytes_hash(file_bytes)
                    try:
                        old_hash = [
                            x for x in already_found_links if x.link == zamena.link
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

                            sup.add_already_found_link(
                                link=zamena.link, date=date, hash=file_hash
                            )

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
    except Exception as e:
        print(e)
        return CheckResultError(
            result="Error",
            trace=Html.escape(str(traceback.format_exc())[0:100]),
            error=Html.escape(str(e)),
        ).model_dump()
