import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from events import add_event  # noqa: E402
from users import add_user  # noqa: E402
from bookings import cancel_booking, create_booking, is_available  # noqa: E402


def make_event(seats=10):
    events = []
    add_event(events, "Мероприятие", "2026-10-15", "Место", seats, 500)
    return events[0]


def make_user(name="Иван"):
    users = []
    add_user(users, name)
    return users[0]


def test_create_booking_success():
    event = make_event(seats=10)
    user = make_user()
    bookings = []
    booking = create_booking(bookings, event, user, 3)
    assert booking is not None
    assert len(bookings) == 1


def test_create_booking_not_enough_seats():
    event = make_event(seats=2)
    user = make_user()
    bookings = []
    booking = create_booking(bookings, event, user, 5)
    assert booking is None


def test_cancel_booking_frees_seats():
    event = make_event(seats=5)
    user = make_user()
    bookings = []
    booking = create_booking(bookings, event, user, 5)
    assert not is_available(bookings, event, 1)

    cancel_booking(bookings, booking.id)
    assert is_available(bookings, event, 5)


def test_booking_str_representation():
    event = make_event(seats=5)
    user = make_user("Иван")
    bookings = []
    booking = create_booking(bookings, event, user, 2)
    assert "Иван" in str(booking)
    assert "подтверждено" in str(booking)

    booking.cancel()
    assert "отменено" in str(booking)
