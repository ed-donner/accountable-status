"""Reads and writes on the checks and incidents tables. Every function takes a connection."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import case, func, insert, select, update
from sqlalchemy.engine import Connection

from .db import checks, incidents


def insert_check(
    conn: Connection, service_id: str, checked_at: datetime, up: bool, response_ms: int | None
) -> int:
    """Store one check. A down check never carries a response time."""
    if not up:
        response_ms = None
    elif response_ms is None:
        raise ValueError("an up check needs a response time")
    result = conn.execute(
        insert(checks).values(service_id=service_id, checked_at=checked_at, up=up, response_ms=response_ms)
    )
    return int(result.inserted_primary_key[0])


def find_open_incident(conn: Connection, service_id: str) -> dict[str, Any] | None:
    row = conn.execute(
        select(incidents)
        .where(incidents.c.service_id == service_id, incidents.c.closed_at.is_(None))
        .order_by(incidents.c.opened_at.desc())
        .limit(1)
    ).mappings().first()
    return dict(row) if row else None


def open_incident(conn: Connection, service_id: str, opened_at: datetime) -> int:
    result = conn.execute(insert(incidents).values(service_id=service_id, opened_at=opened_at, closed_at=None))
    return int(result.inserted_primary_key[0])


def close_incident(conn: Connection, incident_id: int, closed_at: datetime) -> None:
    conn.execute(
        update(incidents)
        .where(incidents.c.id == incident_id, incidents.c.closed_at.is_(None))
        .values(closed_at=closed_at)
    )


def latest_check(conn: Connection, service_id: str) -> dict[str, Any] | None:
    row = conn.execute(
        select(checks)
        .where(checks.c.service_id == service_id)
        .order_by(checks.c.checked_at.desc(), checks.c.id.desc())
        .limit(1)
    ).mappings().first()
    return dict(row) if row else None


def count_checks(conn: Connection) -> int:
    return int(conn.execute(select(func.count()).select_from(checks)).scalar_one())


def checks_between(
    conn: Connection, service_id: str, start: datetime, end: datetime
) -> list[dict[str, Any]]:
    """Checks with start <= checked_at < end, oldest first."""
    rows = conn.execute(
        select(checks)
        .where(checks.c.service_id == service_id, checks.c.checked_at >= start, checks.c.checked_at < end)
        .order_by(checks.c.checked_at, checks.c.id)
    ).mappings()
    return [dict(r) for r in rows]


def check_counts_between(conn: Connection, service_id: str, start: datetime, end: datetime) -> tuple[int, int]:
    """(total checks, up checks) with start <= checked_at < end."""
    row = conn.execute(
        select(func.count(), func.coalesce(func.sum(case((checks.c.up.is_(True), 1), else_=0)), 0)).where(
            checks.c.service_id == service_id, checks.c.checked_at >= start, checks.c.checked_at < end
        )
    ).one()
    return int(row[0]), int(row[1])


def recent_checks(conn: Connection, service_id: str, now: datetime, hours: int = 24) -> list[dict[str, Any]]:
    """Checks from the last `hours` hours up to now, oldest first."""
    return checks_between(conn, service_id, now - timedelta(hours=hours), now + timedelta(seconds=1))


def list_incidents(conn: Connection, service_id: str, limit: int = 200) -> list[dict[str, Any]]:
    """Incidents, newest first."""
    rows = conn.execute(
        select(incidents)
        .where(incidents.c.service_id == service_id)
        .order_by(incidents.c.opened_at.desc(), incidents.c.id.desc())
        .limit(limit)
    ).mappings()
    return [dict(r) for r in rows]
