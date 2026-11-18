"""SQLAlchemy Core tables and engine setup for the SQLite file."""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Index,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    event,
)
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.types import TypeDecorator

log = logging.getLogger(__name__)


class UtcDateTime(TypeDecorator):
    """Stores times as naive UTC and hands them back as aware UTC."""

    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value: datetime | None, dialect):
        if value is None:
            return None
        if value.tzinfo is None:
            raise ValueError("times must carry a timezone")
        return value.astimezone(UTC).replace(tzinfo=None)

    def process_result_value(self, value: datetime | None, dialect):
        if value is None:
            return None
        return value.replace(tzinfo=UTC)


metadata = MetaData()

checks = Table(
    "checks",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("service_id", String(64), nullable=False),
    Column("checked_at", UtcDateTime, nullable=False),
    Column("up", Boolean, nullable=False),
    # Blank for a down check (FR1.3).
    Column("response_ms", Integer, nullable=True),
)
Index("ix_checks_service_checked_at", checks.c.service_id, checks.c.checked_at)

incidents = Table(
    "incidents",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("service_id", String(64), nullable=False),
    Column("opened_at", UtcDateTime, nullable=False),
    # Blank while the incident is open (FR2.4).
    Column("closed_at", UtcDateTime, nullable=True),
)
Index("ix_incidents_service_opened_at", incidents.c.service_id, incidents.c.opened_at)


def make_engine(database_path: Path | str) -> Engine:
    """Create the engine, making the folder if needed."""
    path = Path(database_path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except OSError:
        log.exception("Could not create the database folder %s", path.parent)
        raise
    engine = create_engine(f"sqlite:///{path}", connect_args={"timeout": 15})

    @event.listens_for(engine, "connect")
    def _pragmas(dbapi_connection, _record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.close()

    return engine


def create_schema(engine: Engine) -> None:
    try:
        metadata.create_all(engine)
    except SQLAlchemyError:
        log.exception("Could not create the database tables")
        raise
