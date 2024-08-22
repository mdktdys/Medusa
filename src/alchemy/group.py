from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped

from .base import Base


class Group(Base):
    __tablename__: str = "Groups"

    name: Mapped[str]
    department: Mapped[int]
