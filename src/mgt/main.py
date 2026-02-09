from __future__ import annotations

import os

from mgt.core.config import Settings
from mgt.core.job_runner import run_scan_job
from mgt.core.logging_config import configure_logging
from mgt.ops.disk_monitor import check_disk_and_alert
from mgt.ops.log_cleanup import cleanup_logs
from mgt.scanning.sqlalchemy_scanner import SQLAlchemyMetadataScanner


def main() -> None:
    settings = Settings.from_env()
    configure_logging(settings)

    os.makedirs(settings.metadb_dir, exist_ok=True)
    os.makedirs(settings.log_dir, exist_ok=True)

    scanner = SQLAlchemyMetadataScanner(source_db_url=settings.source_db_url)

    # One-off scan
    job_id = run_scan_job(
        metadb_url=settings.meta_db_url,
        scanner=scanner,
        source_db_url=settings.source_db_url,
    )
    print(f"Scan job completed: {job_id}")

    # Ops: disk + cleanup
    check_disk_and_alert(settings)
    cleanup_logs(settings)


if __name__ == "__main__":
    main()
