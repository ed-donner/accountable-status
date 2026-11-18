"""Incident rules: open on the first failed check, close on the first success."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy.engine import Connection

from . import repository


def record_result(
    conn: Connection, service_id: str, checked_at: datetime, up: bool, response_ms: int | None
) -> str | None:
    """Store a check and update the incident. Returns "opened", "closed" or None."""
    repository.insert_check(conn, service_id, checked_at, up, response_ms)
    open_one = repository.find_open_incident(conn, service_id)
    if not up and open_one is None:
        repository.open_incident(conn, service_id, checked_at)
        return "opened"
    if up and open_one is not None:
        repository.close_incident(conn, open_one["id"], checked_at)
        return "closed"
    return None
