import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models import Event, User, Booking  # noqa: E402


def test_event_creation():
    event = Event(1, "Ревизор", "2026-10-15", "Театр", 50, 800)
    assert event.id == 1
    assert event.name == "Ревизор"
    assert event.seats == 50


def test_event_has_capacity():
    event = Event(1, "Ревизор", "2026-10-15", "Театр", 10, 800)
    assert event.has_capacity(booked_seats=5, tickets_count=5)
    assert not event.has_capacity(booked_seats=5, tickets_count=6)


def test_user_creation():
    user = User(1, "Иван Петров")
    assert user.id == 1
    assert user.name == "Иван Петров"


def test_booking_creation_and_cancel():
    event = Event(1, "Ревизор", "2026-10-15", "Театр", 50, 800)
    user = User(1, "Иван Петров")
    booking = Booking(1, event, user, 2)

    assert booking.event is event
    assert booking.user is user
    assert not booking.is_cancelled

    booking.cancel()
    assert booking.is_cancelled
