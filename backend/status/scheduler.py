"""A loop inside the backend that checks every service on an interval."""

from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime

import httpx
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from . import incidents
from .checker import check_service
from .config import Service

log = logging.getLogger(__name__)


def _store(engine: Engine, service_id: str, checked_at: datetime, up: bool, response_ms: int | None) -> str | None:
    with engine.begin() as conn:
        return incidents.record_result(conn, service_id, checked_at, up, response_ms)


async def run_once(engine: Engine, services: tuple[Service, ...], timeout: float, client: httpx.AsyncClient) -> None:
    """Check every service once and store the results. Failures are logged, never raised."""
    for service in services:
        checked_at = datetime.now(UTC)
        try:
            result = await check_service(service, timeout, client)
            event = await asyncio.to_thread(_store, engine, service.id, checked_at, result.up, result.response_ms)
        except (SQLAlchemyError, OSError):
            log.exception("Could not store the check for %s", service.id)
            continue
        except Exception:
            log.exception("Check failed for %s", service.id)
            continue
        log.info("%s: %s%s", service.id, "up" if result.up else "down", f" (incident {event})" if event else "")


async def run_forever(engine: Engine, services: tuple[Service, ...], interval: float, timeout: float) -> None:
    """Run a check now and then every `interval` seconds until cancelled."""
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=False) as client:
        while True:
            started = asyncio.get_running_loop().time()
            await run_once(engine, services, timeout, client)
            elapsed = asyncio.get_running_loop().time() - started
            await asyncio.sleep(max(0.0, interval - elapsed))
