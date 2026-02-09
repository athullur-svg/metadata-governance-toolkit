from __future__ import annotations

from dataclasses import asdict
from typing import Iterable, Iterator

from mgt.scanning.sqlalchemy_scanner import ColumnMeta


def to_data_dictionary_rows(
    columns: Iterable[ColumnMeta],
    system_name: str = "local",
) -> Iterator[dict]:
    for c in columns:
        d = asdict(c)
        yield {
            "system_name": system_name,
            "database_name": d["database_name"],
            "schema_name": d["schema_name"],
            "object_name": d["object_name"],
            "object_type": d["object_type"],
            "column_name": d["column_name"],
            "data_type": d["data_type"],
            "nullable": d["nullable"],
        }
