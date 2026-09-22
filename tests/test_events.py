import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from events import add_event, find_event, sort_events_by_date  # noqa: E402


def test_add_event():
    events = []
    event = add_event(events, "Ревизор", "2026-10-15", "Театр", 50, 800)
    assert len(events) == 1
    assert event.name == "Ревизор"


def test_find_event():
    events = []
    add_event(events, "Ревизор", "2026-10-15", "Театр", 50, 800)
    found = find_event(events, 1)
    assert found is not None
    assert found.name == "Ревизор"


def test_find_event_not_found():
    events = []
    assert find_event(events, 999) is None


def test_sort_events_by_date():
    events = []
    add_event(events, "Позже", "2026-12-01", "Место", 10, 100)
    add_event(events, "Раньше", "2026-10-01", "Место", 10, 100)
    sorted_events = sort_events_by_date(events)
    assert sorted_events[0].name == "Раньше"
