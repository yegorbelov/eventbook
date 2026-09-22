from typing import List, Optional

from models import Booking, Event, User


def is_available(bookings: List[Booking], event: Event, tickets_count: int) -> bool:
    booked = sum(
        b.tickets_count for b in bookings
        if b.event.id == event.id and not b.is_cancelled
    )
    return event.has_capacity(booked, tickets_count)


def create_booking(
    bookings: List[Booking], event: Event, user: User, tickets_count: int
) -> Optional[Booking]:
    if not is_available(bookings, event, tickets_count):
        return None

    booking_id = len(bookings) + 1
    booking = Booking(booking_id, event, user, tickets_count)
    bookings.append(booking)
    return booking


def cancel_booking(bookings: List[Booking], booking_id: int) -> bool:
    for booking in bookings:
        if booking.id == booking_id:
            booking.cancel()
            return True
    return False


def show_bookings(bookings: List[Booking]) -> None:
    if not bookings:
        print("Бронирований пока нет.")
        return
    for booking in bookings:
        print(booking)
