import httpx
from sqlalchemy import select

from status import repository, scheduler
from status.config import Service
from status.db import checks


async def test_a_run_stores_a_check_and_opens_then_closes_an_incident(engine, stand_in_factory):
    page = stand_in_factory()
    api = stand_in_factory(status=401)
    service = Service("accountable", "Accountable", page.url, api.url)
    async with httpx.AsyncClient(timeout=1) as client:
        await scheduler.run_once(engine, (service,), 1, client)
        api.stop()
        await scheduler.run_once(engine, (service,), 1, client)
        with engine.connect() as conn:
            (open_one,) = repository.list_incidents(conn, "accountable")
        assert open_one["closed_at"] is None
        replacement = stand_in_factory()
        service_back = Service("accountable", "Accountable", page.url, replacement.url)
        await scheduler.run_once(engine, (service_back,), 1, client)
    with engine.connect() as conn:
        (incident,) = repository.list_incidents(conn, "accountable")
        ups = [r[0] for r in conn.execute(select(checks.c.up).order_by(checks.c.id))]
    assert incident["closed_at"] is not None
    assert ups == [True, False, True]
