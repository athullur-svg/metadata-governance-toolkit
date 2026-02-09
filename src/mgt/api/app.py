from __future__ import annotations

from fastapi import FastAPI
from mgt.api.routes import router

app = FastAPI(title="Metadata Governance Toolkit", version="0.1.0")
app.include_router(router)
