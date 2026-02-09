from __future__ import annotations

import hashlib


def stable_hash(*parts: str) -> str:
    """
    Stable SHA-256 hash for idempotent keys.
    Normalizes by stripping and lowercasing.
    """
    normalized = "|".join((p or "").strip().lower() for p in parts)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
