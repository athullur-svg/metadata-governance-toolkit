from __future__ import annotations

import datetime as dt
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, Integer, Text


class Base(DeclarativeBase):
    pass


class ScanJob(Base):
    __tablename__ = "scan_job"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    job_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    source_db_url: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(16))  # RUNNING/SUCCESS/FAILED
    started_at: Mapped[dt.datetime] = mapped_column(DateTime, default=dt.datetime.utcnow)
    finished_at: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)


class DataDictionaryRow(Base):
    __tablename__ = "data_dictionary"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hash_key: Mapped[str] = mapped_column(String(64), unique=True, index=True)

    system_name: Mapped[str] = mapped_column(String(128), default="local")
    database_name: Mapped[str] = mapped_column(String(128))
    schema_name: Mapped[str] = mapped_column(String(128))
    object_name: Mapped[str] = mapped_column(String(256))  # table/view
    object_type: Mapped[str] = mapped_column(String(32))   # TABLE/VIEW
    column_name: Mapped[str] = mapped_column(String(256))
    data_type: Mapped[str] = mapped_column(String(128))
    nullable: Mapped[str] = mapped_column(String(8))       # Y/N

    updated_at: Mapped[dt.datetime] = mapped_column(DateTime, default=dt.datetime.utcnow)
