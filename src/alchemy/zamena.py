import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .course import Course


class Zamena(Base):
    __tablename__: str = "Zamenas"

    id: Mapped[int] = mapped_column(primary_key=True)
    group: Mapped[int]
    number: Mapped[int]
    course: Mapped[int] = mapped_column(ForeignKey("Courses.id"))
    course_model: Mapped["Course"] = relationship(back_populates="Zamenas")
    teacher: Mapped[int]
    cabinet: Mapped[int]
    date: Mapped[datetime.datetime]
