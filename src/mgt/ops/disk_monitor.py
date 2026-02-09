from __future__ import annotations

import logging
import os
import psutil
from mgt.core.config import Settings

log = logging.getLogger(__name__)


def check_disk_and_alert(settings: Settings) -> None:
    """
    Checks disk usage where LOG_DIR lives.
    If above threshold, logs a warning (you can later wire email/slack).
    """
    path = os.path.abspath(settings.log_dir)
    usage = psutil.disk_usage(path)
    used_ratio = usage.used / usage.total

    log.info("Disk usage at %s: %.2f%%", path, used_ratio * 100)

    if used_ratio >= settings.disk_alert_threshold:
        log.warning(
            "DISK ALERT: usage %.2f%% >= threshold %.2f%% (path=%s)",
            used_ratio * 100,
            settings.disk_alert_threshold * 100,
            path,
        )
