"""Daily uptime in local time and the bar colors."""

from __future__ import annotations

from datetime import UTC, date, datetime, time, timedelta
from typing import Literal

from sqlalchemy.engine import Connection

from . import repository

Color = Literal["green", "amber", "red", "grey"]

GREEN_AT = 99.9
AMBER_AT = 99.0


def bar_color(uptime: float | None) -> Color:
    """Compare unrounded: 99.9 is green, 99.0 is amber. None means no checks that day."""
    if uptime is None:
        return "grey"
    if uptime >= GREEN_AT:
        return "green"
    if uptime >= AMBER_AT:
        return "amber"
    return "red"


def local_day_start(day: date) -> datetime:
    """Local midnight at the start of `day`, as an aware datetime (handles daylight saving)."""
    return datetime.combine(day, time.min).astimezone()


def daily_uptime(
    conn: Connection, service_id: str, now: datetime, days: int = 90
) -> list[dict]:
    """One entry per local day, oldest first, ending with today (counted so far)."""
    today = now.astimezone().date()
    result = []
    for offset in range(days - 1, -1, -1):
        day = today - timedelta(days=offset)
        start = local_day_start(day)
        end = local_day_start(day + timedelta(days=1))
        total, up = repository.check_counts_between(conn, service_id, start.astimezone(UTC), end.astimezone(UTC))
        uptime = (up / total * 100.0) if total else None
        result.append({"date": day.isoformat(), "uptime": uptime, "color": bar_color(uptime), "checks": total})
    return result


def overall_uptime(daily: list[dict]) -> float | None:
    """Weighted by checks; days with no checks are left out."""
    total = sum(d["checks"] for d in daily)
    if not total:
        return None
    up = sum(d["uptime"] / 100.0 * d["checks"] for d in daily if d["uptime"] is not None)
    return up / total * 100.0
