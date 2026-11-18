from datetime import timedelta

from status import repository

from .conftest import T0


def test_open_incident_is_found_until_closed(engine):
    with engine.begin() as conn:
        assert repository.find_open_incident(conn, "accountable") is None
        incident_id = repository.open_incident(conn, "accountable", T0)
        found = repository.find_open_incident(conn, "accountable")
        assert found["id"] == incident_id
        repository.close_incident(conn, incident_id, T0 + timedelta(minutes=5))
        assert repository.find_open_incident(conn, "accountable") is None


def test_checks_come_back_in_order_for_a_day_and_the_last_24_hours(engine):
    with engine.begin() as conn:
        for minutes in (30, 10, 20):
            repository.insert_check(conn, "accountable", T0 - timedelta(minutes=minutes), True, 100)
        repository.insert_check(conn, "accountable", T0 - timedelta(hours=30), True, 100)
        repository.insert_check(conn, "other", T0 - timedelta(minutes=5), True, 100)
    with engine.connect() as conn:
        recent = repository.recent_checks(conn, "accountable", T0)
        assert [c["checked_at"] for c in recent] == [T0 - timedelta(minutes=m) for m in (30, 20, 10)]
        total, up = repository.check_counts_between(conn, "accountable", T0 - timedelta(hours=1), T0)
        assert (total, up) == (3, 3)


def test_incidents_are_listed_newest_first(engine):
    with engine.begin() as conn:
        repository.open_incident(conn, "accountable", T0 - timedelta(days=2))
        repository.open_incident(conn, "accountable", T0 - timedelta(days=1))
    with engine.connect() as conn:
        rows = repository.list_incidents(conn, "accountable")
    assert [r["opened_at"] for r in rows] == [T0 - timedelta(days=1), T0 - timedelta(days=2)]
