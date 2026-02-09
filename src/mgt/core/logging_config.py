from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler
from mgt.core.config import Settings


def configure_logging(settings: Settings) -> None:
    os.makedirs(settings.log_dir, exist_ok=True)

    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    root = logging.getLogger()
    root.setLevel(level)

    # Avoid duplicate handlers in reload
    if root.handlers:
        return

    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        filename=os.path.join(settings.log_dir, "app.log"),
        maxBytes=2_000_000,
        backupCount=5,
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    root.addHandler(console)
    root.addHandler(file_handler)
