from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    meta_db_url: str
    source_db_url: str
    log_dir: str
    log_level: str
    scheduler_enabled: bool
    scan_interval_minutes: int
    disk_alert_threshold: float
    log_retention_days: int

    @property
    def metadb_dir(self) -> str:
        # Works for sqlite:///./.metadb/metadb.sqlite
        return "./.metadb"

    @staticmethod
    def from_env() -> "Settings":
        load_dotenv()

        def env(key: str, default: str) -> str:
            return os.getenv(key, default)

        def env_bool(key: str, default: str) -> bool:
            return env(key, default).strip().lower() in {"1", "true", "yes", "y"}

        def env_int(key: str, default: str) -> int:
            return int(env(key, default))

        def env_float(key: str, default: str) -> float:
            return float(env(key, default))

        return Settings(
            meta_db_url=env("META_DB_URL", "sqlite:///./.metadb/metadb.sqlite"),
            source_db_url=env("SOURCE_DB_URL", "sqlite:///./.metadb/source_demo.sqlite"),
            log_dir=env("LOG_DIR", "./logs"),
            log_level=env("LOG_LEVEL", "INFO"),
            scheduler_enabled=env_bool("SCHEDULER_ENABLED", "true"),
            scan_interval_minutes=env_int("SCAN_INTERVAL_MINUTES", "60"),
            disk_alert_threshold=env_float("DISK_ALERT_THRESHOLD", "0.75"),
            log_retention_days=env_int("LOG_RETENTION_DAYS", "7"),
        )
