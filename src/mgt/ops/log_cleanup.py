from __future__ import annotations

import logging
import os
import time
from pathlib import Path

from mgt.core.config import Settings

log = logging.getLogger(__name__)


def cleanup_logs(settings: Settings) -> int:
    """
    Deletes log files older than LOG_RETENTION_DAYS from LOG_DIR.
    Returns number of deleted files.
    """
    log_dir = Path(settings.log_dir)
    if not log_dir.exists():
        return 0

    cutoff = time.time() - (settings.log_retention_days * 86400)
    deleted = 0

    for p in log_dir.glob("*.log*"):
        try:
            if p.is_file() and p.stat().st_mtime < cutoff:
                p.unlink()
                deleted += 1
        except Exception:
            log.exception("Failed to delete log file: %s", str(p))

    if deleted:
        log.info("Log cleanup removed %s file(s) older than %s days", deleted, settings.log_retention_days)
    return deleted
