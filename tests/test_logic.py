"""Tests for logic.py + an AppTest smoke run of the Streamlit app."""
from datetime import date
from pathlib import Path

import pytest

from logic import (
    DATA_VINTAGE,
    ELAPSED_DAYS,
    LABS,
    REF_DEFAULT,
    days_since,
    lab_view,
    month_starts,
    sort_labs,
    timeline_points,
    validate_labs,
    x_ticks,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_data_invariants_hold():
    assert validate_labs() == []
    assert DATA_VINTAGE == REF_DEFAULT


def test_latest_is_derived_from_dots():
    for lab in LABS:
        assert lab["latest"] == lab["dots"][-1]
        assert lab["dots"] == sorted(lab["dots"])


def test_chinese_avg_matches_readme_formula():
    for lab in LABS:
        if lab["region"] == "CN":
            assert lab["avg"] == round(ELAPSED_DAYS / len(lab["dots"]))


def test_days_since_reference():
    meta = next(lab for lab in LABS if lab["id"] == "meta")
    assert days_since(meta, date(2026, 10, 13)) == 1
    assert days_since(meta, date(2026, 10, 12)) == 0
    assert days_since(meta, date(2026, 10, 11)) == -1


def test_days_since_invalid_date_returns_none():
    assert days_since({"latest": (2, 30)}, date(2026, 10, 13)) is None


def test_sort_orders():
    ordered = sort_labs(LABS, "Lab order")
    assert ordered == LABS

    fresh = sort_labs(LABS, "Freshest first")
    fresh_days = [days_since(lab, REF_DEFAULT) for lab in fresh]
    known = [d for d in fresh_days if d is not None]
    assert known == sorted(known)

    stale = sort_labs(LABS, "Longest wait first")
    stale_days = [days_since(lab, REF_DEFAULT) for lab in stale]
    known_stale = [d for d in stale_days if d is not None]
    assert known_stale == sorted(known_stale, reverse=True)


def test_lab_view_fields():
    meta = next(lab for lab in LABS if lab["id"] == "meta")
    v = lab_view(meta, date(2026, 10, 13))
    assert v["display"] == "1"
    assert v["status"] in {"✅ on pace", "⚠ overdue"}
    assert 0 <= v["fill"] <= 100
    future = lab_view(meta, date(2026, 9, 1))
    assert future["display"] == "–"
    assert future["status"] == "—"


def test_fill_is_capped():
    meta = next(lab for lab in LABS if lab["id"] == "meta")
    v = lab_view(meta, date(2026, 12, 31))
    assert v["fill"] == 100.0


def test_month_starts_2026():
    starts = month_starts(2026)
    assert starts[0] == ("Jan", 1)
    assert starts[1] == ("Feb", 32)  # 31 days in Jan
    assert starts[11] == ("Dec", 335)
    assert [x for _, x in starts] == sorted(x for _, x in starts)


def test_x_ticks_are_never_duplicated():
    # Jan 1 reference used to emit two ticks at position 1 (bug).
    xs, labels = x_ticks(2026, date(2026, 1, 1))
    assert xs == [1]
    assert labels == ["Today"]

    xs, labels = x_ticks(2026, date(2026, 10, 13))
    assert xs == sorted(set(xs))
    assert len(xs) == len(labels)
    assert labels[-1] == "Today"
    assert "Jan" in labels


def test_timeline_points_window():
    meta = next(lab for lab in LABS if lab["id"] == "meta")
    pts = timeline_points(meta, date(2026, 10, 13))
    assert pts == sorted(pts)
    assert all(1 <= p <= 286 for p in pts)
    # Dots after the reference date are excluded.
    early = timeline_points(meta, date(2026, 9, 1))
    assert all(px <= (date(2026, 9, 1) - date(2026, 1, 1)).days + 1 for px in early)


def test_app_renders_without_exception():
    pytest.importorskip("streamlit")
    from streamlit.testing.v1 import AppTest

    app = AppTest.from_file(str(REPO_ROOT / "streamlit_app.py"), default_timeout=60)
    app.run()
    assert not app.exception, app.exception
