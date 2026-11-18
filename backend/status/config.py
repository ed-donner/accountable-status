"""Settings, read from environment variables so tests can use their own."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_API_PORT = 8790
DEFAULT_WEB_PORT = 5190
CHECK_INTERVAL_SECONDS = 60.0
CHECK_TIMEOUT_SECONDS = 5.0
HISTORY_DAYS = 90

ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Service:
    """A service the status page watches. It is up only when page and api both answer."""

    id: str
    name: str
    page_url: str
    api_url: str


DEFAULT_SERVICES: tuple[Service, ...] = (
    Service(
        id="accountable",
        name="Accountable",
        page_url="http://localhost:5173",
        api_url="http://localhost:8765/api/meta",
    ),
)


class ConfigError(ValueError):
    """An environment variable holds a value that cannot be used."""


def parse_targets(raw: str | None, defaults: tuple[Service, ...] = DEFAULT_SERVICES) -> tuple[Service, ...]:
    """Apply a STATUS_TARGETS override: {"<service id>": {"page": url, "api": url}}."""
    if not raw:
        return defaults
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ConfigError(f"STATUS_TARGETS is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ConfigError("STATUS_TARGETS must be a JSON object keyed by service id")
    known = {s.id: s for s in defaults}
    unknown = set(data) - set(known)
    if unknown:
        raise ConfigError(f"STATUS_TARGETS names unknown services: {sorted(unknown)}")
    services = []
    for service in defaults:
        override = data.get(service.id)
        if override is None:
            services.append(service)
            continue
        if not isinstance(override, dict):
            raise ConfigError(f"STATUS_TARGETS entry for {service.id} must be an object")
        page = override.get("page", service.page_url)
        api = override.get("api", service.api_url)
        if not all(isinstance(u, str) and u.startswith(("http://", "https://")) for u in (page, api)):
            raise ConfigError(f"STATUS_TARGETS addresses for {service.id} must be http or https URLs")
        services.append(Service(service.id, service.name, page, api))
    return tuple(services)


def _positive_float(name: str, default: float) -> float:
    raw = os.environ.get(name)
    if raw is None or raw == "":
        return default
    try:
        value = float(raw)
    except ValueError as exc:
        raise ConfigError(f"{name} must be a number, got {raw!r}") from exc
    if value <= 0:
        raise ConfigError(f"{name} must be above zero, got {raw!r}")
    return value


@dataclass(frozen=True)
class Settings:
    database_path: Path = field(default_factory=lambda: ROOT / "data" / "status.db")
    services: tuple[Service, ...] = DEFAULT_SERVICES
    check_interval: float = CHECK_INTERVAL_SECONDS
    check_timeout: float = CHECK_TIMEOUT_SECONDS
    run_checker: bool = True
    seed_on_empty: bool = True

    @classmethod
    def from_env(cls) -> Settings:
        db = os.environ.get("STATUS_DB")
        return cls(
            database_path=Path(db) if db else ROOT / "data" / "status.db",
            services=parse_targets(os.environ.get("STATUS_TARGETS")),
            check_interval=_positive_float("STATUS_CHECK_INTERVAL", CHECK_INTERVAL_SECONDS),
            check_timeout=_positive_float("STATUS_CHECK_TIMEOUT", CHECK_TIMEOUT_SECONDS),
        )
