from __future__ import annotations

from fastapi import APIRouter
from sqlalchemy import select

from mgt.core.config import Settings
from mgt.core.job_runner import run_scan_job
from mgt.metadb.db import make_engine, make_session_factory
from mgt.metadb.models import Base, ScanJob, DataDictionaryRow
from mgt.metadb.repository import MetaRepository
from mgt.scanning.sqlalchemy_scanner import SQLAlchemyMetadataScanner
from mgt.api.schemas import TriggerScanResponse, ScanJobOut, DataDictionaryOut

router = APIRouter()
settings = Settings.from_env()


def _init_metadb() -> None:
    engine = make_engine(settings.meta_db_url)
    Base.metadata.create_all(engine)
    engine.dispose()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/scan/trigger", response_model=TriggerScanResponse)
def trigger_scan():
    _init_metadb()
    scanner = SQLAlchemyMetadataScanner(source_db_url=settings.source_db_url)
    job_id = run_scan_job(
        metadb_url=settings.meta_db_url,
        scanner=scanner,
        source_db_url=settings.source_db_url,
    )
    return TriggerScanResponse(job_id=job_id)


@router.get("/jobs", response_model=list[ScanJobOut])
def list_jobs(limit: int = 50):
    _init_metadb()
    SessionFactory = make_session_factory(settings.meta_db_url)
    with SessionFactory() as session:
        repo = MetaRepository(session)
        jobs = repo.list_jobs(limit=limit)

        return [
            ScanJobOut(
                job_id=j.job_id,
                status=j.status,
                source_db_url=j.source_db_url,
                started_at=j.started_at.isoformat(),
                finished_at=j.finished_at.isoformat() if j.finished_at else None,
                error_message=j.error_message,
            )
            for j in jobs
        ]


@router.get("/dictionary", response_model=list[DataDictionaryOut])
def list_dictionary(limit: int = 200):
    _init_metadb()
    SessionFactory = make_session_factory(settings.meta_db_url)
    with SessionFactory() as session:
        rows = session.scalars(
            select(DataDictionaryRow).order_by(DataDictionaryRow.id.desc()).limit(limit)
        ).all()

        return [
            DataDictionaryOut(
                system_name=r.system_name,
                database_name=r.database_name,
                schema_name=r.schema_name,
                object_name=r.object_name,
                object_type=r.object_type,
                column_name=r.column_name,
                data_type=r.data_type,
                nullable=r.nullable,
                updated_at=r.updated_at.isoformat(),
            )
            for r in rows
        ]
