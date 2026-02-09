from __future__ import annotations

import logging
import uuid

from sqlalchemy.orm import Session

from mgt.metadb.db import make_engine, make_session_factory
from mgt.metadb.models import Base
from mgt.metadb.repository import MetaRepository
from mgt.transform.data_dictionary import to_data_dictionary_rows
from mgt.scanning.sqlalchemy_scanner import SQLAlchemyMetadataScanner

log = logging.getLogger(__name__)


def _init_metadb(meta_db_url: str) -> None:
    engine = make_engine(meta_db_url)
    Base.metadata.create_all(engine)
    engine.dispose()


def run_scan_job(
    metadb_url: str,
    scanner: SQLAlchemyMetadataScanner,
    source_db_url: str,
) -> str:
    _init_metadb(metadb_url)

    job_id = uuid.uuid4().hex[:16]
    SessionFactory = make_session_factory(metadb_url)

    with SessionFactory() as session:  # type: Session
        repo = MetaRepository(session)
        repo.create_job(job_id=job_id, source_db_url=source_db_url)

        try:
            cols = list(scanner.scan())
            rows = to_data_dictionary_rows(cols, system_name="local")

            for r in rows:
                repo.upsert_dictionary_row(r)

            repo.mark_job_success(job_id)
            log.info("Scan job succeeded job_id=%s rows_scanned=%s", job_id, len(cols))
            return job_id

        except Exception as e:
            repo.mark_job_failed(job_id, str(e))
            log.exception("Scan job failed job_id=%s", job_id)
            raise
