from datetime import time
from typing import Optional

from sqlalchemy import Column, Integer, MetaData, String, Table, Time
from sqlalchemy.orm import DeclarativeBase

from src.alchemy.database import ForeignKey, Mapped, mapped_column, relationship

convention: dict[str, str] = {
    "ix": "ix_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

class Base(DeclarativeBase):
    metadata: MetaData = metadata
    pass


class Specialization(Base):
    __tablename__ = "specializations"
    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String, nullable = False)
    code: Mapped[str] = mapped_column(String, nullable = False)

    groups = relationship("Group", back_populates="specialization")


class Department(Base):
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement = True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique = True)

    groups = relationship("Group", back_populates="department")
    teachers = relationship("Teacher", back_populates="department")


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable = False, unique = True)
    course: Mapped[int] = mapped_column(Integer, nullable = False, default = 1)

    department_id: Mapped[int] = mapped_column(Integer, ForeignKey("departments.id"), nullable = False)
    department: Mapped[Department] = relationship("Department", back_populates="groups")

    specialization_id: Mapped[int] = mapped_column(Integer, ForeignKey("specializations.id"), nullable = False)
    specialization: Mapped[Specialization] = relationship("Specialization", back_populates = "groups")
    

class Teacher(Base):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String, nullable = False)

    department_id: Mapped[int] = mapped_column(Integer, ForeignKey("departments.id"), nullable = False)
    department: Mapped[Department] = relationship("Department", back_populates = "teachers")


class Cabinet(Base):
    __tablename__ = "cabinets"
    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String, nullable = False)
    ceil: Mapped[int] = mapped_column(Integer, nullable = True)
    

search_items_view = Table(
    "search_items",
    Base.metadata,
    Column("uid", String, primary_key=True),
    Column("name", String),
)

class SearchItem(Base):
    __table__: Table = search_items_view
    

class Timings(Base):
    __tablename__ = 'timings'

    number: Mapped[int] = mapped_column(Integer, primary_key=True)
    start: Mapped[time] = mapped_column(Time)
    saturday_start: Mapped[time] = mapped_column(Time)
    saturday_end: Mapped[time] = mapped_column(Time)
    end: Mapped[Optional[time]] = mapped_column(Time)
    obed_start: Mapped[Optional[time]] = mapped_column(Time)
    obed_end: Mapped[Optional[time]] = mapped_column(Time)
    
    
class DisciplineCodes(Base):
    __tablename__ = 'discipline_codes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String, nullable = False)


class Discipline(Base):
    __tablename__ = 'disciplines'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    code_id: Mapped[int] = mapped_column(Integer, ForeignKey("discipline_codes.id"), nullable = True)
    code: Mapped[DisciplineCodes] = relationship("DisciplineCodes", back_populates="disciplines")
    

