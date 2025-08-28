from datetime import time
from typing import List, Optional

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Boolean, Column, Integer, MetaData, String, Table, Time
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import DeclarativeBase

from src.alchemy.database import ForeignKey, Mapped, mapped_column, relationship

convention: dict[str, str] = {
    'ix': 'ix_%(table_name)s_%(column_0_name)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

metadata = MetaData(naming_convention=convention)

class Base(DeclarativeBase):
    metadata: MetaData = metadata
    pass


class Specialization(Base):
    __tablename__ = 'specializations'
    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String, nullable = False)
    code: Mapped[str] = mapped_column(String, nullable = False)

    groups: Mapped[List["Group"]] = relationship('Group', back_populates='specialization')


class Department(Base):
    __tablename__ = 'departments'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement = True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique = True)

    groups: Mapped[List["Group"]] = relationship('Group', back_populates='department')
    teachers: Mapped[List["Teacher"]] = relationship('Teacher', back_populates='department')


class Group(Base):
    __tablename__ = 'groups'
    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable = False, unique = True)
    course: Mapped[int] = mapped_column(Integer, nullable = False, default = 1)

    department_id: Mapped[int] = mapped_column(Integer, ForeignKey('departments.id'), nullable = False)
    department: Mapped[Department] = relationship('Department', back_populates='groups')

    specialization_id: Mapped[int] = mapped_column(Integer, ForeignKey('specializations.id'), nullable = False)
    specialization: Mapped[Specialization] = relationship('Specialization', back_populates='groups')
    

class Teacher(Base):
    __tablename__ = 'teachers'
    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String, nullable = False)

    department_id: Mapped[int] = mapped_column(Integer, ForeignKey('departments.id'), nullable = False)
    department: Mapped[Department] = relationship('Department', back_populates='teachers')


class Cabinet(Base):
    __tablename__ = 'cabinets'
    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String, nullable = False)
    ceil: Mapped[int] = mapped_column(Integer, nullable = True)
    

search_items_view = Table(
    'search_items',
    Base.metadata,
    Column('uid', String, primary_key=True),
    Column('name', String),
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

    code_id: Mapped[int] = mapped_column(Integer, ForeignKey('discipline_codes.id'), nullable = True)
    code: Mapped[DisciplineCodes] = relationship('DisciplineCodes', back_populates='disciplines')
    

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = 'users'
    email: Mapped[str] = mapped_column(String, unique = True, index = True, nullable = True)
    hashed_password: Mapped[str] = mapped_column(String, nullable = True)
    is_active: Mapped[bool] = mapped_column(Boolean, default = True, nullable = False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default = False, nullable = False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default = False, nullable = False)
    role: Mapped[str] = mapped_column(String, default = 'Guest', nullable = False)
    username: Mapped[Optional[str]] = mapped_column(String, default = None, nullable = True)

    telegram_id: Mapped[Optional[str]] = mapped_column(String, default = None, nullable = True)
    chat_id: Mapped[Optional[str]] = mapped_column(String, default = None, nullable = True)
    photo_url: Mapped[Optional[bytes]] = mapped_column(BYTEA, default = None, nullable = True)
    first_name: Mapped[Optional[str]] = mapped_column(String, default = None, nullable = True)
    last_name: Mapped[Optional[str]] = mapped_column(String, default = None, nullable = True)

    align_search_item_uid: Mapped[Optional[str]] = mapped_column(String, ForeignKey('search_items.uid'), nullable=True)
    align_search_item: Mapped[Optional[SearchItem]] = relationship(
        'SearchItem',
        primaryjoin="foreign(User.align_search_item_uid) == remote(SearchItem.uid)",
        viewonly=True,
        lazy='joined',
    )

    favourite_search_items: Mapped[List['FavouriteUserSearchItem']] = relationship(
        'FavouriteUserSearchItem', back_populates='user', cascade='all, delete-orphan'
    )
    

class FavouriteUserSearchItem(Base):
    __tablename__ = 'favourite_user_search_items'

    user_uid: Mapped[str] = mapped_column(String, ForeignKey('users.id'), primary_key=True)
    search_item_uid: Mapped[str] = mapped_column(String, ForeignKey('search_items.uid'), primary_key=True)

    user: Mapped[User] = relationship('User', back_populates='favourite_search_items')
    search_item: Mapped[SearchItem] = relationship('SearchItem', viewonly=True, lazy='joined')