from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def make_engine(db_url: str):
    return create_engine(db_url, future=True)


def make_session_factory(db_url: str):
    engine = make_engine(db_url)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
