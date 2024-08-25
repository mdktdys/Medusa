import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Paras(Base):
    __tablename__: str = "Paras"

    id: Mapped[int] = mapped_column(primary_key=True)
    group: Mapped[int]
    number: Mapped[int]
    course: Mapped[int] = mapped_column(ForeignKey("Courses.id"))
    teacher: Mapped[int]
    cabinet: Mapped[int]
    date: Mapped[datetime.datetime]
