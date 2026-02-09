from __future__ import annotations

import datetime as dt
import logging
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from mgt.core.hashing import stable_hash
from mgt.metadb.models import DataDictionaryRow, ScanJob

log = logging.getLogger(__name__)


class MetaRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_job(self, job_id: str, source_db_url: str) -> None:
        self.session.add(
            ScanJob(
                job_id=job_id,
                source_db_url=source_db_url,
                status="RUNNING",
                started_at=dt.datetime.utcnow(),
            )
        )
        self.session.commit()

    def mark_job_success(self, job_id: str) -> None:
        job = self.session.scalar(select(ScanJob).where(ScanJob.job_id == job_id))
        if not job:
            return
        job.status = "SUCCESS"
        job.finished_at = dt.datetime.utcnow()
        self.session.commit()

    def mark_job_failed(self, job_id: str, error_message: str) -> None:
        job = self.session.scalar(select(ScanJob).where(ScanJob.job_id == job_id))
        if not job:
            return
        job.status = "FAILED"
        job.finished_at = dt.datetime.utcnow()
        job.error_message = error_message
        self.session.commit()

    def upsert_dictionary_row(self, row: dict) -> None:
        hash_key = stable_hash(
            row["system_name"],
            row["database_name"],
            row["schema_name"],
            row["object_name"],
            row["column_name"],
        )

        existing = self.session.scalar(
            select(DataDictionaryRow).where(DataDictionaryRow.hash_key == hash_key)
        )

        if existing:
            # idempotent update
            existing.object_type = row["object_type"]
            existing.data_type = row["data_type"]
            existing.nullable = row["nullable"]
            existing.updated_at = dt.datetime.utcnow()
            self.session.commit()
            return

        # insert
        new_row = DataDictionaryRow(
            hash_key=hash_key,
            system_name=row["system_name"],
            database_name=row["database_name"],
            schema_name=row["schema_name"],
            object_name=row["object_name"],
            object_type=row["object_type"],
            column_name=row["column_name"],
            data_type=row["data_type"],
            nullable=row["nullable"],
            updated_at=dt.datetime.utcnow(),
        )
        self.session.add(new_row)
        try:
            self.session.commit()
        except IntegrityError:
            # race-safe fallback
            self.session.rollback()
            log.warning("IntegrityError on insert; likely concurrent insert. hash=%s", hash_key)

    def list_jobs(self, limit: int = 50):
        stmt = select(ScanJob).order_by(ScanJob.id.desc()).limit(limit)
        return self.session.scalars(stmt).all()

    def list_dictionary(self, limit: int = 200):
        stmt = select(DataDictionaryRow).order_by(DataDictionaryRow.id.desc()).limit(limit)
        return self.session.scalars(stmt).all()
