from typing import List, Optional

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    Double,
    ForeignKeyConstraint,
    Identity,
    Integer,
    Numeric,
    PrimaryKeyConstraint,
    SmallInteger,
    String,
    Table,
    Text,
    Time,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import OID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime


class Base(DeclarativeBase):
    pass


class Cabinets(Base):
    __tablename__ = "Cabinets"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="Cabinets_pkey"),
        UniqueConstraint("name", name="Cabinets_name_key"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=9223372036854775807,
            cycle=False,
            cache=1,
        ),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(Text)

    Paras: Mapped[List["Paras"]] = relationship("Paras", back_populates="Cabinets_")
    Zamenas: Mapped[List["Zamenas"]] = relationship(
        "Zamenas", back_populates="Cabinets_"
    )


class Courses(Base):
    __tablename__ = "Courses"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="Courses_pkey"),
        UniqueConstraint("name", name="Courses_name_key"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    color: Mapped[str] = mapped_column(String)
    name: Mapped[Optional[str]] = mapped_column(Text, server_default=text("''::text"))
    fullname: Mapped[Optional[str]] = mapped_column(String)

    Paras: Mapped[List["Paras"]] = relationship("Paras", back_populates="Courses_")
    Zamenas: Mapped[List["Zamenas"]] = relationship(
        "Zamenas", back_populates="Courses_"
    )


class Departments(Base):
    __tablename__ = "Departments"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="Departments_pkey"),
        UniqueConstraint("name", name="Departments_name_key"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=9223372036854775807,
            cycle=False,
            cache=1,
        ),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(Text, server_default=text("'None'::text"))

    Groups: Mapped[List["Groups"]] = relationship(
        "Groups", back_populates="Departments_"
    )


class Holidays(Base):
    __tablename__ = "Holidays"
    __table_args__ = (PrimaryKeyConstraint("id", name="Holidays_pkey"),)

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=9223372036854775807,
            cycle=False,
            cache=1,
        ),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(Text)
    date: Mapped[Optional[datetime.date]] = mapped_column(Date)


class MessagingClients(Base):
    __tablename__ = "MessagingClients"
    __table_args__ = (PrimaryKeyConstraint("id", name="MessagingClients_pkey"),)

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=9223372036854775807,
            cycle=False,
            cache=1,
        ),
        primary_key=True,
    )
    token: Mapped[str] = mapped_column(
        String, server_default=text("'-1'::character varying")
    )
    clientID: Mapped[Optional[int]] = mapped_column(
        SmallInteger, server_default=text("'-1'::smallint")
    )
    subType: Mapped[Optional[int]] = mapped_column(
        SmallInteger, server_default=text("'-1'::smallint")
    )
    subID: Mapped[Optional[int]] = mapped_column(SmallInteger)


class Subscribers(Base):
    __tablename__ = "Subscribers"
    __table_args__ = (PrimaryKeyConstraint("id", name="Subscribers_pkey"),)

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=9223372036854775807,
            cycle=False,
            cache=1,
        ),
        primary_key=True,
    )
    chat_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    target_type: Mapped[Optional[int]] = mapped_column(SmallInteger)
    target_id: Mapped[Optional[int]] = mapped_column(BigInteger)


class Teachers(Base):
    __tablename__ = "Teachers"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="Teachers_pkey"),
        UniqueConstraint("name", name="Teachers_name_key"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(String)

    Paras: Mapped[List["Paras"]] = relationship("Paras", back_populates="Teachers_")
    Zamenas: Mapped[List["Zamenas"]] = relationship(
        "Zamenas", back_populates="Teachers_"
    )


class ZamenaFileLinks(Base):
    __tablename__ = "ZamenaFileLinks"
    __table_args__ = (PrimaryKeyConstraint("id", name="ZamenaFileLinks_pkey"),)

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=9223372036854775807,
            cycle=False,
            cache=1,
        ),
        primary_key=True,
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(True), server_default=text("now()")
    )
    link: Mapped[Optional[str]] = mapped_column(Text)
    date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    hash: Mapped[Optional[str]] = mapped_column(String)


t_pg_stat_statements = Table(
    "pg_stat_statements",
    Base.metadata,
    Column("userid", OID),
    Column("dbid", OID),
    Column("toplevel", Boolean),
    Column("queryid", BigInteger),
    Column("query", Text),
    Column("plans", BigInteger),
    Column("total_plan_time", Double(53)),
    Column("min_plan_time", Double(53)),
    Column("max_plan_time", Double(53)),
    Column("mean_plan_time", Double(53)),
    Column("stddev_plan_time", Double(53)),
    Column("calls", BigInteger),
    Column("total_exec_time", Double(53)),
    Column("min_exec_time", Double(53)),
    Column("max_exec_time", Double(53)),
    Column("mean_exec_time", Double(53)),
    Column("stddev_exec_time", Double(53)),
    Column("rows", BigInteger),
    Column("shared_blks_hit", BigInteger),
    Column("shared_blks_read", BigInteger),
    Column("shared_blks_dirtied", BigInteger),
    Column("shared_blks_written", BigInteger),
    Column("local_blks_hit", BigInteger),
    Column("local_blks_read", BigInteger),
    Column("local_blks_dirtied", BigInteger),
    Column("local_blks_written", BigInteger),
    Column("temp_blks_read", BigInteger),
    Column("temp_blks_written", BigInteger),
    Column("blk_read_time", Double(53)),
    Column("blk_write_time", Double(53)),
    Column("temp_blk_read_time", Double(53)),
    Column("temp_blk_write_time", Double(53)),
    Column("wal_records", BigInteger),
    Column("wal_fpi", BigInteger),
    Column("wal_bytes", Numeric),
    Column("jit_functions", BigInteger),
    Column("jit_generation_time", Double(53)),
    Column("jit_inlining_count", BigInteger),
    Column("jit_inlining_time", Double(53)),
    Column("jit_optimization_count", BigInteger),
    Column("jit_optimization_time", Double(53)),
    Column("jit_emission_count", BigInteger),
    Column("jit_emission_time", Double(53)),
)


t_pg_stat_statements_info = Table(
    "pg_stat_statements_info",
    Base.metadata,
    Column("dealloc", BigInteger),
    Column("stats_reset", DateTime(True)),
)


class ScheduleTimetable(Base):
    __tablename__ = "scheduleTimetable"
    __table_args__ = (
        PrimaryKeyConstraint("number", name="scheduleTimetable_pkey"),
        UniqueConstraint("number", name="scheduleTimetable_number_key"),
    )

    number: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    saturdayStart: Mapped[str] = mapped_column(Text)
    saturdayEnd: Mapped[str] = mapped_column(Text)
    start: Mapped[Optional[str]] = mapped_column(Text)
    end: Mapped[Optional[str]] = mapped_column(Text)
    obedStart: Mapped[Optional[str]] = mapped_column(Text)
    obedEnd: Mapped[Optional[str]] = mapped_column(Text)

    Paras: Mapped[List["Paras"]] = relationship(
        "Paras", back_populates="scheduleTimetable"
    )
    Zamenas: Mapped[List["Zamenas"]] = relationship(
        "Zamenas", back_populates="scheduleTimetable"
    )


class Timings(Base):
    __tablename__ = "timings"
    __table_args__ = (
        PrimaryKeyConstraint("number", name="timings_pkey"),
        UniqueConstraint("number", name="timings_number_key"),
        {"comment": "This is a duplicate of scheduleTimetable"},
    )

    number: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    start: Mapped[datetime.time] = mapped_column(Time)
    saturdayStart: Mapped[datetime.time] = mapped_column(Time)
    saturdayEnd: Mapped[datetime.time] = mapped_column(Time)
    end: Mapped[Optional[datetime.time]] = mapped_column(Time)
    obedStart: Mapped[Optional[datetime.time]] = mapped_column(Time)
    obedEnd: Mapped[Optional[datetime.time]] = mapped_column(Time)


class Groups(Base):
    __tablename__ = "Groups"
    __table_args__ = (
        ForeignKeyConstraint(
            ["department"], ["Departments.id"], name="Groups_department_fkey"
        ),
        PrimaryKeyConstraint("id", name="Groups_pkey"),
        UniqueConstraint("name", name="Groups_name_key"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=9223372036854775807,
            cycle=False,
            cache=1,
        ),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(String(10), server_default=text("''::text"))
    department: Mapped[Optional[int]] = mapped_column(BigInteger)

    Departments_: Mapped["Departments"] = relationship(
        "Departments", back_populates="Groups"
    )
    Liquidation: Mapped[List["Liquidation"]] = relationship(
        "Liquidation", back_populates="Groups_"
    )
    Paras: Mapped[List["Paras"]] = relationship("Paras", back_populates="Groups_")
    Practices: Mapped[List["Practices"]] = relationship(
        "Practices", back_populates="Groups_"
    )
    Zamenas: Mapped[List["Zamenas"]] = relationship("Zamenas", back_populates="Groups_")
    ZamenasFull: Mapped[List["ZamenasFull"]] = relationship(
        "ZamenasFull", back_populates="Groups_"
    )


class Liquidation(Base):
    __tablename__ = "Liquidation"
    __table_args__ = (
        ForeignKeyConstraint(
            ["group"], ["Groups.id"], name="public_Liquidation_group_fkey"
        ),
        PrimaryKeyConstraint("id", name="Liquidation_pkey"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=9223372036854775807,
            cycle=False,
            cache=1,
        ),
        primary_key=True,
    )
    group: Mapped[int] = mapped_column(BigInteger)
    date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    Groups_: Mapped["Groups"] = relationship("Groups", back_populates="Liquidation")


class Paras(Base):
    __tablename__ = "Paras"
    __table_args__ = (
        ForeignKeyConstraint(["cabinet"], ["Cabinets.id"], name="Paras_cabinet_fkey"),
        ForeignKeyConstraint(["course"], ["Courses.id"], name="Paras_course_fkey"),
        ForeignKeyConstraint(["group"], ["Groups.id"], name="Paras_group_fkey"),
        ForeignKeyConstraint(
            ["number"], ["scheduleTimetable.number"], name="Paras_number_fkey"
        ),
        ForeignKeyConstraint(["teacher"], ["Teachers.id"], name="Paras_teacher_fkey"),
        PrimaryKeyConstraint("id", name="Paras_pkey"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=9223372036854775807,
            cycle=False,
            cache=1,
        ),
        primary_key=True,
    )
    group: Mapped[Optional[int]] = mapped_column(BigInteger)
    number: Mapped[Optional[int]] = mapped_column(BigInteger)
    course: Mapped[Optional[int]] = mapped_column(BigInteger)
    teacher: Mapped[Optional[int]] = mapped_column(BigInteger)
    cabinet: Mapped[Optional[int]] = mapped_column(BigInteger)
    date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    Cabinets_: Mapped["Cabinets"] = relationship("Cabinets", back_populates="Paras")
    Courses_: Mapped["Courses"] = relationship(
        "Courses", back_populates="Paras", lazy="selectin"
    )
    Groups_: Mapped["Groups"] = relationship("Groups", back_populates="Paras")
    scheduleTimetable: Mapped["ScheduleTimetable"] = relationship(
        "ScheduleTimetable", back_populates="Paras"
    )
    Teachers_: Mapped["Teachers"] = relationship("Teachers", back_populates="Paras")


class Practices(Base):
    __tablename__ = "Practices"
    __table_args__ = (
        ForeignKeyConstraint(
            ["group"], ["Groups.id"], name="public_Practices_group_fkey"
        ),
        PrimaryKeyConstraint("id", name="Practices_pkey"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=9223372036854775807,
            cycle=False,
            cache=1,
        ),
        primary_key=True,
    )
    group: Mapped[Optional[int]] = mapped_column(BigInteger)
    date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    Groups_: Mapped["Groups"] = relationship("Groups", back_populates="Practices")


class Zamenas(Base):
    __tablename__ = "Zamenas"
    __table_args__ = (
        ForeignKeyConstraint(["cabinet"], ["Cabinets.id"], name="Zamenas_cabinet_fkey"),
        ForeignKeyConstraint(["course"], ["Courses.id"], name="Zamenas_course_fkey"),
        ForeignKeyConstraint(["group"], ["Groups.id"], name="Zamenas_group_fkey"),
        ForeignKeyConstraint(
            ["number"], ["scheduleTimetable.number"], name="Zamenas_number_fkey"
        ),
        ForeignKeyConstraint(["teacher"], ["Teachers.id"], name="Zamenas_teacher_fkey"),
        PrimaryKeyConstraint("id", name="lesons_pkey"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=9223372036854775807,
            cycle=False,
            cache=1,
        ),
        primary_key=True,
    )
    group: Mapped[Optional[int]] = mapped_column(BigInteger)
    teacher: Mapped[Optional[int]] = mapped_column(BigInteger)
    course: Mapped[Optional[int]] = mapped_column(BigInteger)
    number: Mapped[Optional[int]] = mapped_column(BigInteger)
    date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    cabinet: Mapped[Optional[int]] = mapped_column(BigInteger)

    Cabinets_: Mapped["Cabinets"] = relationship("Cabinets", back_populates="Zamenas")
    Courses_: Mapped["Courses"] = relationship(
        "Courses", back_populates="Zamenas", lazy="selectin"
    )
    Groups_: Mapped["Groups"] = relationship("Groups", back_populates="Zamenas")
    scheduleTimetable: Mapped["ScheduleTimetable"] = relationship(
        "ScheduleTimetable", back_populates="Zamenas"
    )
    Teachers_: Mapped["Teachers"] = relationship("Teachers", back_populates="Zamenas")


class ZamenasFull(Base):
    __tablename__ = "ZamenasFull"
    __table_args__ = (
        ForeignKeyConstraint(
            ["group"], ["Groups.id"], name="public_ZamenasFull_group_fkey"
        ),
        PrimaryKeyConstraint("id", name="ZamenasFull_pkey"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=9223372036854775807,
            cycle=False,
            cache=1,
        ),
        primary_key=True,
    )
    group: Mapped[int] = mapped_column(BigInteger)
    date: Mapped[datetime.date] = mapped_column(Date, server_default=text("now()"))

    Groups_: Mapped["Groups"] = relationship("Groups", back_populates="ZamenasFull")
