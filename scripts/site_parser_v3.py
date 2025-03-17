import asyncio
import datetime
import ssl
import string
import urllib
from typing import List
from urllib.parse import quote
from urllib.request import urlopen

import bs4
import certifi
# from src.parser.models.zamena_table_model import ZamTable

from bs4 import BeautifulSoup, PageElement

from src.models.zamena_model import Zamena
from src.parser.models.zamena_table_model import ZamTable


def get_zamena_tables():
    def define_month(string_: str) -> int | None:
        string_ = string_.split(' ')[0].lower()
        months = [
            "январь",
            "февраль",
            "март",
            "апрель",
            "май",
            "июнь",
            "июль",
            "август",
            "сентябрь",
            "октябрь",
            "ноябрь",
            "декабрь",
        ]
        return months.index(string_) + 1

    def define_year(string_: str) -> int | None:
        string_separated = string_.split(' ')

        if len(string_separated) == 1:
            return datetime.datetime.now().year

        return int(string_separated[1].lower())

    context = ssl.create_default_context(cafile=certifi.where())
    url = "https://uksivt.ru/"
    response = urlopen(url + quote('замены'), context=context)
    soup = BeautifulSoup(response.read(), "html.parser")
    tables = soup.find_all(name="table", attrs={"class": "has-fixed-layout"})
    zamena_tables = []
    for table in tables[0:2]:
        zamenas: List[Zamena] = []
        rows = table.find_all('tr')
        hyper_link_texts: List[PageElement] = table.find_all('a')
        header_text = rows[0].text
        month = define_month(header_text)
        year = define_year(header_text)

        for link in hyper_link_texts:
            text = link.get_text()
            if text.isdigit():
                if link:
                    date = datetime.date(year, month, int(text))
                    zamena_link = urllib.parse.urljoin("https://www.uksivt.ru/zameny/", link.get("href"))
                    zamenas.append(Zamena(link=zamena_link, date=date))
        zamena_tables.append(ZamTable(raw=table, month_index=month, year=year))
    return zamena_tables
