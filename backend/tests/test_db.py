from datetime import timedelta

import pytest
from sqlalchemy import select

from status import repository
from status.db import checks, incidents

from .conftest import T0


def test_check_and_incident_rows_round_trip(engine):
    with engine.begin() as conn:
        repository.insert_check(conn, "accountable", T0, True, 120)
        repository.open_incident(conn, "accountable", T0)
    with engine.connect() as conn:
        check = conn.execute(select(checks)).mappings().one()
        incident = conn.execute(select(incidents)).mappings().one()
    assert check["checked_at"] == T0 and check["up"] is True and check["response_ms"] == 120
    assert incident["opened_at"] == T0 and incident["closed_at"] is None


def test_down_check_stores_no_response_time(engine):
    with engine.begin() as conn:
        repository.insert_check(conn, "accountable", T0, False, 999)
    with engine.connect() as conn:
        assert conn.execute(select(checks.c.response_ms)).scalar_one() is None


def test_up_check_without_response_time_is_refused(engine):
    with engine.begin() as conn, pytest.raises(ValueError):
        repository.insert_check(conn, "accountable", T0 + timedelta(minutes=1), True, None)
