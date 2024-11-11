import asyncio
import datetime

#
from src.parser.parsers import parse_zamenas
from src.parser.supabase import SupaBaseWorker

#
# from src.parser.methods import get_latest_zamena_link
# from src.parser.supabase import SupaBaseWorker
# from src.parser.zamena_parser import get_remote_file_hash

#
url = "https://www.uksivt.ru/storage/files/all/ZAMENY/2024/Ноябрь/11.11.pdf"
date = datetime.date(2024, 11, 11)


async def a():
    res = await parse_zamenas(url=url, date_=date, force=True)
    print(res)


a()
asyncio.run(a())

sup = SupaBaseWorker()


# print(res)
#
# link = "https://www.uksivt.ru//storage/files/all/ документы/Замены 2023/+29.10.pdf"
# file_hash = get_remote_file_hash(url=link)
# sup.add_already_found_link(
#     link=link,
#     date=datetime.date(2024, 10, 30).strftime("%Y-%m-%d"),
#     hash=file_hash,
# )
# /zamena  2024.11.2
