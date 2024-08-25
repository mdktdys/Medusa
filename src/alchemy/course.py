import datetime

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Course(Base):
    __tablename__: str = "Courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int]
    color: Mapped[int]
    fullname: Mapped[int]
