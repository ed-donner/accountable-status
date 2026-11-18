from datetime import timedelta

from status import incidents, repository

from .conftest import T0


def record(engine, minute, up):
    with engine.begin() as conn:
        return incidents.record_result(conn, "accountable", T0 + timedelta(minutes=minute), up, 100 if up else None)


def test_first_failure_opens_one_more_failures_add_none_first_success_closes(engine):
    assert record(engine, 0, True) is None
    assert record(engine, 1, False) == "opened"
    assert record(engine, 2, False) is None
    assert record(engine, 3, False) is None
    with engine.connect() as conn:
        rows = repository.list_incidents(conn, "accountable")
    assert len(rows) == 1 and rows[0]["closed_at"] is None
    assert rows[0]["opened_at"] == T0 + timedelta(minutes=1)

    assert record(engine, 4, True) == "closed"
    assert record(engine, 5, True) is None
    with engine.connect() as conn:
        rows = repository.list_incidents(conn, "accountable")
    assert len(rows) == 1 and rows[0]["closed_at"] == T0 + timedelta(minutes=4)


def test_a_new_failure_after_a_close_opens_a_second_incident(engine):
    record(engine, 0, False)
    record(engine, 1, True)
    assert record(engine, 2, False) == "opened"
    with engine.connect() as conn:
        assert len(repository.list_incidents(conn, "accountable")) == 2
