from __future__ import annotations

from pydantic import BaseModel


class TriggerScanResponse(BaseModel):
    job_id: str


class ScanJobOut(BaseModel):
    job_id: str
    status: str
    source_db_url: str
    started_at: str
    finished_at: str | None
    error_message: str | None


class DataDictionaryOut(BaseModel):
    system_name: str
    database_name: str
    schema_name: str
    object_name: str
    object_type: str
    column_name: str
    data_type: str
    nullable: str
    updated_at: str
