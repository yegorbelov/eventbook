import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from events import add_event
from bookings import (
    cancel_booking,
    create_booking,
    get_booking_status,
    is_available,
)


def make_event(seats=10):
    events = []
    add_event(events, "Мероприятие", "2026-10-15", "Место", seats, 500)
    return events[0]


def test_create_booking_success():
    event = make_event(seats=10)
    bookings = []
    booking = create_booking(bookings, event, "Иван", 3)
    assert booking is not None
    assert len(bookings) == 1


def test_create_booking_not_enough_seats():
    event = make_event(seats=2)
    bookings = []
    booking = create_booking(bookings, event, "Иван", 5)
    assert booking is None


def test_cancel_booking_frees_seats():
    event = make_event(seats=5)
    bookings = []
    booking = create_booking(bookings, event, "Иван", 5)
    assert not is_available(bookings, event, 1)

    cancel_booking(bookings, booking["id"])
    assert is_available(bookings, event, 5)


def test_get_booking_status():
    assert get_booking_status(False) == "подтверждено"
    assert get_booking_status(True) == "отменено"
