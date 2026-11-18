"""The JSON API the status page reads."""

from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import UTC, datetime

from fastapi import FastAPI, HTTPException
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from . import repository, scheduler, seed, stats
from .config import HISTORY_DAYS, Service, Settings
from .db import create_schema, make_engine

log = logging.getLogger(__name__)


def _iso(value: datetime | None) -> str | None:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z") if value else None


def _incident_json(row: dict, now: datetime) -> dict:
    closed = row["closed_at"]
    end = closed or now
    return {
        "id": row["id"],
        "opened_at": _iso(row["opened_at"]),
        "closed_at": _iso(closed),
        "open": closed is None,
        # An open incident counts the time elapsed so far (FR2.4).
        "duration_seconds": max(0, int((end - row["opened_at"]).total_seconds())),
    }


def build_service_status(engine: Engine, service: Service, now: datetime) -> dict:
    with engine.connect() as conn:
        daily = stats.daily_uptime(conn, service.id, now, HISTORY_DAYS)
        recent = repository.recent_checks(conn, service.id, now, 24)
        incident_rows = repository.list_incidents(conn, service.id)
        latest = repository.latest_check(conn, service.id)
    if latest is None:
        state = "unknown"
    else:
        state = "up" if latest["up"] else "down"
    return {
        "id": service.id,
        "name": service.name,
        "state": state,
        "last_checked_at": _iso(latest["checked_at"]) if latest else None,
        "uptime_90d": stats.overall_uptime(daily),
        "days": daily,
        "response_times": [
            {"t": _iso(c["checked_at"]), "ms": c["response_ms"] if c["up"] else None} for c in recent
        ],
        "incidents": [_incident_json(r, now) for r in incident_rows],
    }


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    engine = make_engine(settings.database_path)
    create_schema(engine)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        task = None
        try:
            if settings.seed_on_empty:
                try:
                    seeded = await asyncio.to_thread(seed.seed_if_empty, engine, settings.services)
                except (SQLAlchemyError, OSError):
                    log.exception("Could not fill the empty database with sample history")
                    raise
                if seeded:
                    log.info("Filled the empty database with sample history")
            if settings.run_checker:
                task = asyncio.create_task(
                    scheduler.run_forever(engine, settings.services, settings.check_interval, settings.check_timeout)
                )
            yield
        finally:
            if task is not None:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            engine.dispose()

    app = FastAPI(title="Accountable Status", lifespan=lifespan)
    app.state.engine = engine
    app.state.settings = settings

    @app.get("/api/status")
    async def get_status() -> dict:
        now = datetime.now(UTC)
        try:
            services = await asyncio.gather(
                *(asyncio.to_thread(build_service_status, engine, s, now) for s in settings.services)
            )
        except SQLAlchemyError as exc:
            log.exception("Could not read the status data")
            raise HTTPException(status_code=503, detail="The status data could not be read") from exc
        return {"generated_at": _iso(now), "services": list(services)}

    return app
