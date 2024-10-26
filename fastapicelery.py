import datetime

from src.parser.parsers import parse_zamenas

url = "https://www.uksivt.ru/storage/files/all/ZAMENY/2024/%D0%9E%D0%BA%D1%82%D1%8F%D0%B1%D1%80%D1%8C/24.10.docx.pdf"
date = datetime.date(2024, 10, 24)
res = parse_zamenas(url=url, date_=date, force=True)
print(res)
