import datetime

from sqlalchemy.orm import Mapped

from .base import Base


class Paras(Base):
    __tablename__: str = "Paras"

    group: Mapped[int]
    number: Mapped[int]
    course: Mapped[int]
    teacher: Mapped[int]
    cabinet: Mapped[int]
    date: Mapped[datetime.datetime]
