# import datetime
#
# from src.parser.methods import get_latest_zamena_link
# from src.parser.supabase import SupaBaseWorker
# from src.parser.zamena_parser import get_remote_file_hash

#
# url = "https://www.uksivt.ru//storage/files/all/%20%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B/%D0%97%D0%B0%D0%BC%D0%B5%D0%BD%D1%8B%202024/+30.10.docx.pdf"
# date = datetime.date(2024, 10, 30)
#
#
# async def a():
#     res = await parse   _zamenas(url=url, date_=date, force=True)
#     print(res)
#
#
# a()
# asyncio.run(a())

# sup = SupaBaseWorker()
#
# link = "https://www.uksivt.ru//storage/files/all/ документы/Замены 2023/+29.10.pdf"
# file_hash = get_remote_file_hash(url=link)
# sup.add_already_found_link(
#     link=link,
#     date=datetime.date(2024, 10, 30).strftime("%Y-%m-%d"),
#     hash=file_hash,
# )
