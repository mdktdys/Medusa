from typing import List

from src.alchemy import database


# from src.alchemy import Paras as AlchemyParas
# from src.alchemy import Zamena as AlchemyZamena


class Para:
    origin: database.Paras | None = None
    zamena: database.Zamenas | None = None

    def __init__(self, origin, zamena):
        self.origin = origin
        self.zamena = zamena


class DaySchedule:
    search_name: str
    full_zamena: bool
    paras: List[Para] = []

    def __init__(self, paras, search_name, full_zamena):
        self.paras: List[Para] = paras
        self.search_name: str = search_name
        self.full_zamena: bool = full_zamena
