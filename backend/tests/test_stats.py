import pytest

from status.stats import bar_color, overall_uptime


@pytest.mark.parametrize(
    "uptime, color",
    [(99.95, "green"), (99.5, "amber"), (98.0, "red"), (99.9, "green"), (99.0, "amber"), (100.0, "green"), (None, "grey")],
)
def test_bar_color_thresholds(uptime, color):
    assert bar_color(uptime) == color


def test_just_below_a_threshold_is_not_rounded_up():
    assert bar_color(99.8999) == "amber"
    assert bar_color(98.9999) == "red"


def test_days_with_no_checks_are_left_out_of_overall_uptime():
    days = [
        {"uptime": 100.0, "checks": 100},
        {"uptime": None, "checks": 0},
        {"uptime": 50.0, "checks": 100},
    ]
    assert overall_uptime(days) == 75.0
    assert overall_uptime([{"uptime": None, "checks": 0}]) is None
