import asyncio
import datetime

#
from src.parser.parsers import parse_zamenas, convert_pdf2word, parse_zamenas_from_word
from src.parser.supabase import SupaBaseWorker

from src.parser.methods import get_latest_zamena_link, check_new
from src.parser.supabase import SupaBaseWorker
from src.parser.zamena_parser import get_remote_file_hash


# url = "https://www.uksivt.ru//storage/files/all/ZAMENY/2024/%D0%94%D0%B5%D0%BA%D0%B0%D0%B1%D1%80%D1%8C/20.12.docx.pdf"
# date = datetime.date(2024, 12, 20)
#
#
# #
# #
# async def a():
#     res = await parse_zamenas(url=url, date_=date, force=True)
#     print(res)
#
#
# a()
# asyncio.run(a())
def b():
    asyncio.run(check_new())


def c():
    b()


c()
# sup = SupaBaseWorker()

#
# url = 'https://ojbsikxdqcbuvamygezd.supabase.co/storage/v1/object/sign/zamenas/3.12.pdf?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJ6YW1lbmFzLzMuMTIucGRmIiwiaWF0IjoxNzMzMTQwNTA0LCJleHAiOjE3NjQ2NzY1MDR9.4t-H4UnugKUX8LGhgg9XhYGylQ2Ahc-rClWeUmuO44s&t=2024-12-02T11%3A55%3A04.598Z'
# convert_pdf2word(
#     url=url,
#     file_name="response (3).docx",
# )

from io import BytesIO

#
#
# async def b():
#     with open("response (3).docx", "rb") as fh:
#         buf = BytesIO(fh.read())
#         await parse_zamenas_from_word(
#             url=url,
#             date_=date,
#             file_bytes=buf,
#             force=False,
#         )
#
#
# asyncio.run(b())

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
