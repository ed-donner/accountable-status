from datetime import UTC, datetime
from itertools import groupby

from sqlalchemy import select

from status import seed
from status.config import DEFAULT_SERVICES
from status.db import checks, incidents

NOW = datetime(2026, 11, 18, 9, 30, tzinfo=UTC)


def rows(engine):
    with engine.connect() as conn:
        c = [tuple(r) for r in conn.execute(select(checks.c.checked_at, checks.c.up, checks.c.response_ms).order_by(checks.c.id))]
        i = [tuple(r) for r in conn.execute(select(incidents.c.opened_at, incidents.c.closed_at).order_by(incidents.c.id))]
    return c, i


def test_sample_history_covers_90_days_with_incidents_and_slow_stretches(engine):
    seed.write_history(engine, DEFAULT_SERVICES, NOW)
    check_rows, incident_rows = rows(engine)
    assert len(check_rows) > 89 * 1440
    up_share = sum(1 for r in check_rows if r[1]) / len(check_rows)
    assert up_share > 0.99  # mostly up
    closed = [(c - o).total_seconds() for o, c in incident_rows if c is not None]
    assert len(closed) >= 3 and len(set(closed)) >= 3
    ups = [r for r in check_rows if r[1]]
    assert all(r[2] is not None for r in ups) and all(r[2] is None for r in check_rows if not r[1])
    runs = [len(list(g)) for slow, g in groupby(ups, key=lambda r: r[2] >= 1200) if slow]
    assert len([n for n in runs if n >= 20]) >= 2
    normal = [r[2] for r in ups if r[2] < 1200]
    assert min(normal) >= 80 and max(normal) <= 250


def test_seeding_twice_gives_the_same_data(engine):
    seed.write_history(engine, DEFAULT_SERVICES, NOW)
    first = rows(engine)
    seed.write_history(engine, DEFAULT_SERVICES, NOW)
    assert rows(engine) == first


def test_seed_if_empty_leaves_existing_data_alone(engine):
    assert seed.seed_if_empty(engine, DEFAULT_SERVICES, NOW) is True
    assert seed.seed_if_empty(engine, DEFAULT_SERVICES, NOW) is False


def test_seed_command_asks_first_and_declining_changes_nothing(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("STATUS_DB", str(tmp_path / "cli.db"))
    assert seed.main([], input_fn=lambda prompt: "n") == 0
    assert "Nothing changed" in capsys.readouterr().out
    assert not (tmp_path / "cli.db").exists()
    assert seed.main([], input_fn=lambda prompt: "y") == 0
    assert (tmp_path / "cli.db").exists()
