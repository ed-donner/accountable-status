import httpx

from status.checker import check_service
from status.config import Service


def make_service(page, api):
    return Service("accountable", "Accountable", page, api)


async def test_both_answer_including_401_is_up_with_the_slower_time(stand_in_factory):
    page = stand_in_factory(status=200, delay=0.02)
    api = stand_in_factory(status=401, delay=0.25)
    result = await check_service(make_service(page.url, api.url), timeout=5)
    assert result.up is True
    assert result.response_ms >= 240  # the API was slower, so its time is the one kept


async def test_one_address_stopped_is_down_with_no_time(stand_in_factory):
    page = stand_in_factory()
    api = stand_in_factory()
    api.stop()
    result = await check_service(make_service(page.url, api.url), timeout=5)
    assert result.up is False
    assert result.response_ms is None


async def test_no_answer_within_the_timeout_counts_as_down(stand_in_factory):
    page = stand_in_factory()
    api = stand_in_factory(delay=1.5)
    async with httpx.AsyncClient(timeout=0.3) as client:
        result = await check_service(make_service(page.url, api.url), timeout=0.3, client=client)
    assert result.up is False
    assert result.response_ms is None
