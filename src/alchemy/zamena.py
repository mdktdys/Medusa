import datetime

from sqlalchemy.orm import Mapped

from .base import Base


class Zamena(Base):
    __tablename__: str = "Zamenas"

    group: Mapped[int]
    number: Mapped[int]
    course: Mapped[int]
    teacher: Mapped[int]
    cabinet: Mapped[int]
    date: Mapped[datetime.datetime]
