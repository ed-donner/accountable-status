"""Probe a service. It is up only when both its page and its API answer with any HTTP status."""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass

import httpx

from .config import Service

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class CheckResult:
    up: bool
    response_ms: int | None


async def _probe(client: httpx.AsyncClient, url: str) -> int | None:
    """Milliseconds until any HTTP answer, or None when there is none (error or timeout)."""
    started = time.perf_counter()
    try:
        await client.get(url)
    except httpx.HTTPError as exc:
        log.info("No answer from %s: %s", url, exc.__class__.__name__)
        return None
    except Exception:
        log.exception("Unexpected error probing %s", url)
        return None
    return max(1, round((time.perf_counter() - started) * 1000))


async def check_service(service: Service, timeout: float, client: httpx.AsyncClient | None = None) -> CheckResult:
    """Probe the page and the API together. Down checks store no response time (FR1.3)."""
    owns_client = client is None
    if client is None:
        client = httpx.AsyncClient(timeout=timeout, follow_redirects=False)
    try:
        page_ms, api_ms = await asyncio.gather(_probe(client, service.page_url), _probe(client, service.api_url))
    finally:
        if owns_client:
            await client.aclose()
    if page_ms is None or api_ms is None:
        return CheckResult(up=False, response_ms=None)
    return CheckResult(up=True, response_ms=max(page_ms, api_ms))
