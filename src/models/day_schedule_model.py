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
    paras: List[Para] = []

    def __init__(self, paras):
        self.paras: List[Para] = paras
