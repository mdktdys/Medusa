from typing import List

from src.models.paras_model import Paras


class Para:
    origin: Paras
    zamena: Paras | None = None

    def __init__(self, origin, zamena):
        self.origin = origin
        self.zamena = zamena


class DaySchedule:
    paras: List[Para] = []

    def __init__(self, paras):
        self.paras: List[Para] = paras
