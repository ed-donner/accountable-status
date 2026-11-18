from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

from status import incidents, seed
from status.api import create_app
from status.config import DEFAULT_SERVICES, Settings


def make_client(tmp_path, **kwargs):
    settings = Settings(database_path=tmp_path / "api.db", run_checker=False, **kwargs)
    return TestClient(create_app(settings))


def test_status_returns_90_days_the_24_hour_series_and_incidents(tmp_path):
    with make_client(tmp_path) as client:  # first start fills the empty database
        body = client.get("/api/status").json()
    (service,) = body["services"]
    assert service["id"] == "accountable" and service["name"] == "Accountable"
    assert len(service["days"]) == 90
    assert {d["color"] for d in service["days"]} <= {"green", "amber", "red", "grey"}
    assert len(service["response_times"]) >= 1000
    assert len([i for i in service["incidents"] if not i["open"]]) >= 3
    assert service["state"] == "up"


def test_an_open_incident_counts_its_time_so_far(tmp_path):
    with make_client(tmp_path, seed_on_empty=False) as client:
        engine = client.app.state.engine
        opened = datetime.now(UTC) - timedelta(minutes=10)
        with engine.begin() as conn:
            incidents.record_result(conn, "accountable", opened, False, None)
        service = client.get("/api/status").json()["services"][0]
    assert service["state"] == "down"
    (incident,) = service["incidents"]
    assert incident["open"] is True and incident["closed_at"] is None
    assert 590 <= incident["duration_seconds"] <= 700


def test_empty_database_without_seeding_still_answers(tmp_path):
    with make_client(tmp_path, seed_on_empty=False) as client:
        service = client.get("/api/status").json()["services"][0]
    assert service["state"] == "unknown"
    assert all(d["color"] == "grey" for d in service["days"])
    assert service["uptime_90d"] is None


def test_days_with_downtime_are_not_green(tmp_path):
    with make_client(tmp_path) as client:
        service = client.get("/api/status").json()["services"][0]
    colors = {d["color"] for d in service["days"]}
    assert {"green", "amber", "red"} <= colors
    assert 99.0 < service["uptime_90d"] < 100.0
