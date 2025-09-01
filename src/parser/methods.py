import base64
import datetime
import html as Html
import os
import traceback
from io import BytesIO
from typing import Any, List

from docx2pdf import convert

from parser_v3 import parse_schedule_from_file
from scripts.site_parser_v3 import get_zamena_tables
from src.parser.core import get_all_tables_zamenas, getLastZamenaLink
from src.parser.parsers import parse_zamenas
from src.parser.site_schecker.schemas import (
    CheckResultCheckExisting,
    CheckResultError,
    CheckResultFoundNew,
    CheckZamenaResultFailed,
    CheckZamenaResultFailedDownload,
    CheckZamenaResultInvalidFormat,
    CheckZamenaResultSuccess,
)
from src.parser.supabase import SupaBaseWorker
from src.parser.zamena_parser import (
    create_pdf_screenshots_bytes,
    download_file,
    get_bytes_hash,
    get_file_extension,
    get_remote_file_hash,
)
from src.utils.get_remote_file_bytes import get_remote_file_bytes


async def parse_zamena(url: str, date: datetime.datetime, notify: bool) -> dict:
    return (await parse_zamenas(url=url, date_=date, notify = notify)).model_dump()


# def parse_zamena_json(url: str, date: datetime.datetime, datasource: DataSource) -> dict:
#     return parse_zamenas_json(url=url, date = date, datasource = datasource)


async def parse_group_schedule_v3(file: BytesIO, monday_date: datetime.date) -> dict:
    paras: List = parse_schedule_from_file(file, monday_date)
    json_paras = [paras.model_dump() for paras in paras]
    return {"paras": json_paras}


def get_latest_zamena_link():
    try:
        link, date = getLastZamenaLink()
        return {
            "date": date,
            "link": link
        }
    except Exception as e:
        return {
            "message": "failed",
            "reason": str(e),
            "trace": traceback.format_exc()
        }


async def delete_zamena(date: datetime.date) -> dict[str, Any]:
    try:
        sup = SupaBaseWorker()
        removed = [
            sup.client.table("Zamenas").delete().eq("date", date).execute(),
            sup.client.table("ZamenasFull").delete().eq("date", date).execute(),
            sup.client.table("ZamenaFileLinks").delete().eq("date", date).execute(),
            sup.client.table("Liquidation").delete().eq("date", date).execute(),
            sup.client.table("Practices").delete().eq("date", date).execute(),
            sup.client.table("teacher_cabinet_swaps").delete().eq("date", date).execute()
        ]
        return {
            "res": "ok",
            "removed": str(len(removed))
        }
    except Exception as e:
        return {
            "message": "failed",
            "reason": str(e)
        }


async def check_new() -> dict[str, Any]:
    from src.api_v1.notifications.views import send_message_to_all
    
    try:
        sup = SupaBaseWorker()
        tables = get_zamena_tables()
        site_links = get_all_tables_zamenas(tables)
        already_found_links = sup.get_already_found_links()
        new_links = list(
            set([x.link for x in site_links])
            # - set([x.link for x in database_links])
            - set([x.link for x in already_found_links])
        )
        if len(new_links) != 0:
            new_links.reverse()
            result = CheckResultFoundNew()
            for link in new_links:
                zamena_table = [x for x in tables if x.links.__contains__(link)][0]
                zamena_cell = [x for x in zamena_table.zamenas if x.link == link][0]
                date: str = datetime.datetime(
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
                        await send_message_to_all('Новые замены', f'Появились новые замены на {date}')
                        sup.add_already_found_link(link=link, date=date, hash=None)
                        continue
                    extension = get_file_extension(zamena_cell.link)
                    filename = zamena_cell.link.split("/")[-1].replace(
                        f".{extension}", ""
                    )
                    file_downloaded = download_file(link=zamena_cell.link, filename=f"{filename}.{extension}")
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
                        await send_message_to_all('Новые замены', f'Появились новые замены на {date}')
                        sup.add_already_found_link(link=link, date=date, hash=None)
                        continue

                    file_hash = get_remote_file_hash(url=zamena_cell.link)
                    match extension:
                        case "pdf":
                            screenshot_paths = create_pdf_screenshots_bytes(filename)
                        case "jpeg":
                            with open(f"{filename}.{extension}", "rb") as image_file:
                                data: bytes = base64.b64encode(image_file.read())
                                screenshot_paths = [data]
                        case _:
                            result.checks.append(
                                CheckZamenaResultInvalidFormat(
                                    date=zamena_cell.date,
                                    file=zamena_cell.link,
                                    link=zamena_cell.link,
                                )
                            )
                            await send_message_to_all('Новые замены', f'Появились новые замены на {date}')
                            sup.add_already_found_link(link=link, date=date, hash=file_hash)
                            continue
                    result.checks.append(
                        CheckZamenaResultSuccess(
                            date=zamena_cell.date,
                            images=screenshot_paths,
                            link=zamena_cell.link,
                        )
                    )
                    await send_message_to_all('Новые замены', f'Появились новые замены на {date}')
                    sup.add_already_found_link(link=link, date=date, hash=file_hash)
                    os.remove(f"{filename}.{extension}")
                except Exception as e:
                    result.checks.append(
                        CheckZamenaResultFailed(
                            error=str(e),
                            trace=Html.escape(str(traceback.format_exc())[0:200]),
                        )
                    )
            sup.client.table("checks").insert({"result": "new"}).execute()
            return result.model_dump()
        else:
            print("check in existing links")
            result = CheckResultCheckExisting()
            for zamena in tables[0].zamenas:
                if zamena.date > datetime.date.today():
                    file_bytes = get_remote_file_bytes(link=zamena.link)
                    file_hash = get_bytes_hash(file_bytes)
                    try:
                        old_hash = [x for x in already_found_links if x.link == zamena.link]
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
                            print(f"hash changed {zamena.link}")
                            extension = get_file_extension(zamena.link)
                            filename = zamena.link.split("/")[-1].split(".")[0]
                            file_downloaded = download_file(link=zamena.link, filename=f"{filename}.{extension}")
                            if not file_downloaded:
                                print("Fail to download")
                                print(extension)
                                print(filename)
                                print(zamena.link)
                                result.checks.append(
                                    CheckZamenaResultFailedDownload(
                                        date=zamena.date,
                                        link=zamena.link,
                                    )
                                )
                                await send_message_to_all('Обнаружен перезалив', f'Перезалили замены на {zamena.date}')
                                sup.update_hash_already_found_link(link=zamena.link, new_hash=None)
                                continue
                            match extension:
                                case "pdf":
                                    screenshot_paths = create_pdf_screenshots_bytes(filename)
                                case "docx":
                                    convert(f"{filename}.{extension}")
                                    screenshot_paths = create_pdf_screenshots_bytes(filename)
                                case _:
                                    result.checks.append(
                                        CheckZamenaResultInvalidFormat(
                                            date=zamena.date,
                                            file=zamena.link,
                                            link=zamena.link,
                                        )
                                    )
                                    await send_message_to_all('Обнаружен перезалив', f'Перезалили замены на {zamena.date}')
                                    sup.update_hash_already_found_link(link=zamena.link, new_hash=file_hash)
                                    continue
                            result.checks.append(
                                CheckZamenaResultSuccess(
                                    date=zamena.date,
                                    images=screenshot_paths,
                                    link=zamena.link,
                                )
                            )
                            os.remove(f"{filename}.pdf")
                            await send_message_to_all('Обнаружен перезалив', f'Перезалили замены на {zamena.date}')
                            sup.update_hash_already_found_link(link=zamena.link, new_hash=file_hash)
                    except Exception as e:
                        print(e)
                        return CheckResultError(
                            result="Error",
                            trace=Html.escape(str(traceback.format_exc())[0:100]),
                            error=Html.escape(str(e)),
                        ).model_dump()
            if any([True for check in result.checks if isinstance(check, CheckZamenaResultSuccess)]):
                sup.client.table("checks").insert({"result": "new"}).execute()
            else:
                sup.client.table("checks").insert({"result": "ok"}).execute()
            return result.model_dump()
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return CheckResultError(
            result="Error",
            trace=Html.escape(str(traceback.format_exc())[0:100]),
            error=Html.escape(str(e)),
        ).model_dump()
