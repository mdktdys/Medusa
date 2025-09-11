import uuid
from datetime import date, datetime, time
from enum import Enum as PyEnum
from typing import List, Optional

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Index,
    Integer,
    MetaData,
    String,
    Table,
    Time,
    UniqueConstraint,
)
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import BYTEA, UUID
from sqlalchemy.orm import DeclarativeBase

from src.alchemy.database import ForeignKey, Mapped, func, mapped_column, relationship

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
    commerce: Mapped[bool] = mapped_column(Boolean, nullable = False)

    department_id: Mapped[int] = mapped_column(Integer, ForeignKey('departments.id'), nullable = False)
    department: Mapped[Department] = relationship('Department', back_populates='groups')

    specialization_id: Mapped[int] = mapped_column(Integer, ForeignKey('specializations.id'), nullable = False)
    specialization: Mapped[Specialization] = relationship('Specialization', back_populates='groups')

    load_linkers: Mapped[List['LoadLink']] = relationship('LoadLink', back_populates='group')
    zamena_group: Mapped[List['ZamenaGroup']] = relationship('ZamenaGroup', back_populates='group')
    lessons: Mapped[List['Lesson']] = relationship('Lesson', back_populates='group')
    

class Teacher(Base):
    __tablename__ = 'teachers'
    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String, nullable = False)

    department_id: Mapped[int] = mapped_column(Integer, ForeignKey('departments.id'), nullable = False)
    department: Mapped[Department] = relationship('Department', back_populates='teachers')

    load_linkers: Mapped[List['LoadLink']] = relationship('LoadLink', back_populates='teacher')
    lessons: Mapped[List['Lesson']] = relationship('Lesson', back_populates='teacher')
    zamena_group_swap: Mapped[List['ZamenaGroupSwaps']] = relationship('ZamenaGroupSwaps', back_populates='teacher')


class Cabinet(Base):
    __tablename__ = 'cabinets'
    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String, nullable = False)
    ceil: Mapped[int] = mapped_column(Integer, nullable = True)
    lessons: Mapped[List['Lesson']] = relationship('Lesson', back_populates='cabinet')
    zamena_group_swap: Mapped[List['ZamenaGroupSwaps']] = relationship('ZamenaGroupSwaps', back_populates='cabinet')
    

search_items_view = Table(
    'search_items',
    Base.metadata,
    Column('uid', String, primary_key=True),
    Column('name', String),
    extend_existing=True,
    info={"is_view": True},
)

class SearchItem(Base):
    __table__: Table = search_items_view

# CREATE MATERIALIZED VIEW public.search_items AS
# SELECT (src.kind || ':' || src.id)::text AS uid,
#        src.id,
#        src.name
# FROM (
#   SELECT 'G'::text AS kind, id::text AS id, name FROM public.groups
#   UNION ALL
#   SELECT 'T'::text AS kind, id::text AS id, name FROM public.teachers
#   UNION ALL
#   SELECT 'C'::text AS kind, id::text AS id, name FROM public.cabinets
# ) AS src;

class Timings(Base):
    __tablename__ = 'timings'

    number: Mapped[int] = mapped_column(Integer, primary_key=True)
    start: Mapped[time] = mapped_column(Time)
    saturday_start: Mapped[time] = mapped_column(Time)
    saturday_end: Mapped[time] = mapped_column(Time)
    end: Mapped[Optional[time]] = mapped_column(Time)
    obed_start: Mapped[Optional[time]] = mapped_column(Time)
    obed_end: Mapped[Optional[time]] = mapped_column(Time)
    zamena_group_swap: Mapped[List['ZamenaGroupSwaps']] = relationship('ZamenaGroupSwaps', back_populates='timing')
    lessons: Mapped[List['Lesson']] = relationship('Lesson', back_populates='timing')
    
    
class DisciplineCodes(Base):
    __tablename__ = 'discipline_codes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String, nullable = False)
    load_linkers: Mapped[List['LoadLink']] = relationship('LoadLink', back_populates='discipline_code')


class Discipline(Base):
    __tablename__ = 'disciplines'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    load_linkers: Mapped[List['LoadLink']] = relationship('LoadLink', back_populates='discipline')
    zamena_group_swap: Mapped[List['ZamenaGroupSwaps']] = relationship('ZamenaGroupSwaps', back_populates='discipline')
    lessons: Mapped[List['Lesson']] = relationship('Lesson', back_populates='discipline')


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
    photo_url: Mapped[Optional[str]] = mapped_column(String, default = None, nullable = True)
    first_name: Mapped[Optional[str]] = mapped_column(String, default = None, nullable = True)
    last_name: Mapped[Optional[str]] = mapped_column(String, default = None, nullable = True)

    align_search_item_uid: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    align_search_item: Mapped[Optional[SearchItem]] = relationship(
        'SearchItem',
        primaryjoin="foreign(User.align_search_item_uid) == remote(SearchItem.uid)",
        viewonly=True,
        lazy='joined',
    )

    favourite_search_items: Mapped[List['FavouriteUserSearchItem']] = relationship(
        'FavouriteUserSearchItem', back_populates='user', cascade='all, delete-orphan'
    )
    

class TelegramAuthState(Base):
    __tablename__ = "telegram_auth_states"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid = True), nullable=False, default = uuid.uuid4, primary_key = True)
    token: Mapped[str] = mapped_column(String, nullable = False)
    access_token: Mapped[str] = mapped_column(String, nullable = True)
    refresh_token: Mapped[str] = mapped_column(String, nullable = True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default = func.now())


class FavouriteUserSearchItem(Base):
    __tablename__ = 'favourite_user_search_items'

    user_uid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid = True), ForeignKey('users.id'), primary_key = True)
    search_item_uid: Mapped[str] = mapped_column(String, primary_key = True)

    user: Mapped[User] = relationship('User', back_populates = 'favourite_search_items')
    search_item: Mapped[SearchItem] = relationship(
        'SearchItem',
        primaryjoin="foreign(FavouriteUserSearchItem.search_item_uid) == remote(SearchItem.uid)",
        viewonly = True,
        lazy = 'joined',
    )


class LoadLink(Base):
    __tablename__ = 'load_linkers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_year_hours: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    second_year_hours: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    teacher_id: Mapped[int] = mapped_column(Integer, ForeignKey('teachers.id'), nullable=False)
    teacher: Mapped[Teacher] = relationship('Teacher', back_populates='load_linkers')

    group_id: Mapped[int] = mapped_column(Integer, ForeignKey('groups.id'), nullable=False)
    group: Mapped[Group] = relationship('Group', back_populates='load_linkers')

    discipline_code_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('discipline_codes.id'), nullable=True)
    discipline_code: Mapped[Optional[DisciplineCodes]] = relationship('DisciplineCodes', back_populates='load_linkers')

    discipline_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('disciplines.id'), nullable=True)
    discipline: Mapped[Optional[Discipline]] = relationship('Discipline', back_populates='load_linkers')


class Zamena(Base):
    __tablename__ = 'zamenas'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date_: Mapped[date] = mapped_column(Date, nullable = False)
    saturday_timings: Mapped[bool] = mapped_column(Boolean, default = False)
    file_url: Mapped[str] = mapped_column(String, nullable = True)
    file_hash: Mapped[str] = mapped_column(String, nullable = True)
    zamena_group: Mapped[List['ZamenaGroup']] = relationship('ZamenaGroup', back_populates='zamena')
    
    
class ZamenaGroupType(PyEnum):
    FULL_SWAP = 'full_swap'
    LIQUIDATION = 'liquidation'
    PRACTICE = 'practice'


class ZamenaGroup(Base):
    __tablename__ = 'zamena_group'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[ZamenaGroupType] = mapped_column(SAEnum(ZamenaGroupType, name='zamena_group_type', native_enum = False), nullable=False)

    zamena_id: Mapped[int] = mapped_column(Integer, ForeignKey('zamenas.id'), nullable=False)
    zamena: Mapped[Zamena] = relationship('Zamena', back_populates='zamena_group')

    group_id: Mapped[int] = mapped_column(Integer, ForeignKey('groups.id'), nullable=False)
    group: Mapped[Group] = relationship('Group', back_populates='zamena_group')
    

class ZamenaGroupSwaps(Base):
    __tablename__ = 'zamena_group_swap'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    timing_id: Mapped[int] = mapped_column(Integer, ForeignKey('timings.number'), nullable = True)
    timing: Mapped[Timings] = relationship('Timings', back_populates='zamena_group_swap')
    
    teacher_id: Mapped[int] = mapped_column(Integer, ForeignKey('teachers.id'), nullable = True)
    teacher: Mapped[Teacher] = relationship('Teacher', back_populates='zamena_group_swap')
    
    discipline_id: Mapped[int] = mapped_column(Integer, ForeignKey('disciplines.id'), nullable = True)
    discipline: Mapped[Discipline] = relationship('Discipline', back_populates='zamena_group_swap')
    
    cabinet_id: Mapped[int] = mapped_column(Integer, ForeignKey('cabinets.id'), nullable = True)
    cabinet: Mapped[Cabinet] = relationship('Cabinet', back_populates='zamena_group_swap')
    
    
class Lesson(Base):
    __tablename__ = 'lessons'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date_: Mapped[date] = mapped_column(Date, nullable = False)
    
    timing_id: Mapped[int] = mapped_column(Integer, ForeignKey('timings.number'), nullable = True)
    timing: Mapped[Timings] = relationship('Timings', back_populates='lessons')
    
    teacher_id: Mapped[int] = mapped_column(Integer, ForeignKey('teachers.id'), nullable = True)
    teacher: Mapped[Teacher] = relationship('Teacher', back_populates='lessons')
    
    discipline_id: Mapped[int] = mapped_column(Integer, ForeignKey('disciplines.id'), nullable = True)
    discipline: Mapped[Discipline] = relationship('Discipline', back_populates='lessons')
    
    cabinet_id: Mapped[int] = mapped_column(Integer, ForeignKey('cabinets.id'), nullable = True)
    cabinet: Mapped[Cabinet] = relationship('Cabinet', back_populates='lessons')
    
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey('groups.id'), nullable = True)
    group: Mapped[Group] = relationship('Group', back_populates='lessons')
    
    
class EntityKind(PyEnum):
    GROUP = "G"
    TEACHER = "T"
    CABINET = "C"
    DISCIPLINE = "D"

class EntityAlias(Base):
    __tablename__ = "entity_aliases"
    __table_args__ = (
        UniqueConstraint("kind", "entity_id", "alias_normalized", name="uq_alias_norm_per_entity"),
        Index("ix_entity_alias_norm", "alias_normalized"),
        Index("ix_entity_alias_kind_norm", "kind", "alias_normalized"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    kind: Mapped[EntityKind] = mapped_column(SAEnum(EntityKind, name="entity_kind", native_enum=False), nullable=False)
    entity_id: Mapped[int] = mapped_column(Integer, nullable=False)

    alias: Mapped[str] = mapped_column(String, nullable=False)
    alias_normalized: Mapped[str] = mapped_column(String, nullable=False)