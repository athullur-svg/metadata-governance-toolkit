from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable

from sqlalchemy import create_engine, text, inspect

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class ColumnMeta:
    database_name: str
    schema_name: str
    object_name: str
    object_type: str  # TABLE/VIEW
    column_name: str
    data_type: str
    nullable: str     # Y/N


class SQLAlchemyMetadataScanner:
    """
    Scans tables + columns via SQLAlchemy inspector.
    Works with SQLite + Postgres (and many others).
    """

    def __init__(self, source_db_url: str):
        self.source_db_url = source_db_url

    def _ensure_demo_sqlite(self) -> None:
        if not self.source_db_url.startswith("sqlite"):
            return

        engine = create_engine(self.source_db_url, future=True)
        with engine.begin() as conn:
            conn.execute(text("CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT, email TEXT)"))
            conn.execute(text("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL)"))
        engine.dispose()

    def scan(self) -> Iterable[ColumnMeta]:
        self._ensure_demo_sqlite()
        engine = create_engine(self.source_db_url, future=True)
        inspector = inspect(engine)

        db_name = self._database_name_from_url(self.source_db_url)

        # For SQLite, schemas are not really used. We'll label as "main".
        schemas = inspector.get_schema_names()
        if not schemas:
            schemas = ["main"]

        for schema in schemas:
            try:
                tables = inspector.get_table_names(schema=schema)
                views = inspector.get_view_names(schema=schema)
            except Exception:
                # Some dialects may not support schema parameter; retry without it
                tables = inspector.get_table_names()
                views = inspector.get_view_names()

            for t in tables:
                for col in inspector.get_columns(t, schema=schema if schema != "main" else None):
                    yield ColumnMeta(
                        database_name=db_name,
                        schema_name=schema,
                        object_name=t,
                        object_type="TABLE",
                        column_name=col["name"],
                        data_type=str(col.get("type", "")),
                        nullable="Y" if col.get("nullable", True) else "N",
                    )

            for v in views:
                # view columns are not consistently supported across dialects;
                # we attempt best-effort via get_columns.
                try:
                    cols = inspector.get_columns(v, schema=schema if schema != "main" else None)
                except Exception:
                    cols = []
                for col in cols:
                    yield ColumnMeta(
                        database_name=db_name,
                        schema_name=schema,
                        object_name=v,
                        object_type="VIEW",
                        column_name=col["name"],
                        data_type=str(col.get("type", "")),
                        nullable="Y" if col.get("nullable", True) else "N",
                    )

        engine.dispose()

    @staticmethod
    def _database_name_from_url(url: str) -> str:
        # Simple name extraction
        if url.startswith("sqlite"):
            return "sqlite_demo"
        return "source_db"
