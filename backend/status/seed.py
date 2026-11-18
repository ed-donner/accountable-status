"""Sample history: 90 days of once-a-minute checks and incidents. The same data every run."""

from __future__ import annotations

import argparse
import logging
import random
import sys
from datetime import UTC, datetime, timedelta

from sqlalchemy import delete, insert
from sqlalchemy.engine import Engine

from . import repository
from .config import HISTORY_DAYS, Service, Settings
from .db import checks, create_schema, incidents, make_engine
from .stats import local_day_start

log = logging.getLogger(__name__)

SEED = 90210
NORMAL_MS = (80, 250)
SLOW_MS = (1200, 2600)

# (minutes before the end of the history when it starts, length in minutes)
OUTAGES = [(4 * 1440 + 215, 7), (19 * 1440 + 600, 42), (47 * 1440 + 130, 185), (71 * 1440 + 800, 15), (82 * 1440 + 50, 2)]
SLOW_STRETCHES = [(11 * 1440 + 400, 35), (33 * 1440 + 900, 70), (60 * 1440 + 300, 25)]


def _minute_floor(now: datetime) -> datetime:
    return now.astimezone(UTC).replace(second=0, microsecond=0)


def build_history(service_id: str, now: datetime) -> tuple[list[dict], list[dict]]:
    """Checks and incidents from local midnight 89 days ago up to the minute before `now`."""
    end = _minute_floor(now)
    start = local_day_start(now.astimezone().date() - timedelta(days=HISTORY_DAYS - 1)).astimezone(UTC)
    total_minutes = int((end - start).total_seconds() // 60)
    down: set[int] = set()
    slow: set[int] = set()
    outage_ranges = []
    for before_end, length in OUTAGES:
        first = total_minutes - before_end
        if first < 0:
            continue
        down.update(range(first, first + length))
        outage_ranges.append((first, first + length))
    for before_end, length in SLOW_STRETCHES:
        first = total_minutes - before_end
        if first >= 0:
            slow.update(range(first, first + length))
    rng = random.Random(SEED)
    check_rows = []
    for minute in range(total_minutes):
        at = start + timedelta(minutes=minute)
        # Draw for every minute so the sequence does not depend on which minutes are down.
        normal = rng.randint(*NORMAL_MS)
        slowed = rng.randint(*SLOW_MS)
        if minute in down:
            check_rows.append({"service_id": service_id, "checked_at": at, "up": False, "response_ms": None})
        else:
            ms = slowed if minute in slow else normal
            check_rows.append({"service_id": service_id, "checked_at": at, "up": True, "response_ms": ms})
    incident_rows = []
    for first, last_excl in sorted(outage_ranges):
        incident_rows.append(
            {
                "service_id": service_id,
                "opened_at": start + timedelta(minutes=first),
                "closed_at": start + timedelta(minutes=last_excl),
            }
        )
    return check_rows, incident_rows


def _insert_chunks(conn, table, rows: list[dict], size: int = 5000) -> None:
    for i in range(0, len(rows), size):
        conn.execute(insert(table), rows[i : i + size])


def write_history(engine: Engine, services: tuple[Service, ...], now: datetime | None = None) -> None:
    """Replace everything with the sample history."""
    now = now or datetime.now(UTC)
    with engine.begin() as conn:
        conn.execute(delete(checks))
        conn.execute(delete(incidents))
        for service in services:
            check_rows, incident_rows = build_history(service.id, now)
            _insert_chunks(conn, checks, check_rows)
            _insert_chunks(conn, incidents, incident_rows)


def seed_if_empty(engine: Engine, services: tuple[Service, ...], now: datetime | None = None) -> bool:
    """Fill an empty database. Returns True when it did."""
    with engine.connect() as conn:
        if repository.count_checks(conn) > 0:
            return False
    write_history(engine, services, now)
    return True


def main(argv: list[str] | None = None, input_fn=input) -> int:
    parser = argparse.ArgumentParser(description="Replace all data with sample data.")
    parser.add_argument("--yes", action="store_true", help="do not ask first")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    if not args.yes:
        try:
            answer = input_fn("Replace all data with sample data? (y/N) ")
        except EOFError:
            answer = ""
        if answer.strip().lower() not in ("y", "yes"):
            print("Nothing changed.")
            return 0
    settings = Settings.from_env()
    engine = make_engine(settings.database_path)
    try:
        create_schema(engine)
        write_history(engine, settings.services)
    except Exception:
        log.exception("Could not write the sample data")
        return 1
    finally:
        engine.dispose()
    print(f"Sample data written to {settings.database_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
