def is_available(bookings, event, tickets_count):
    booked = sum(
        b["tickets_count"] for b in bookings
        if b["event_id"] == event["id"] and not b["is_cancelled"]
    )
    return event["seats"] - booked >= tickets_count


def create_booking(bookings, event, user_name, tickets_count):
    if not is_available(bookings, event, tickets_count):
        return None

    booking = {
        "id": len(bookings) + 1,
        "event_id": event["id"],
        "user_name": user_name,
        "tickets_count": tickets_count,
        "is_cancelled": False,
    }
    bookings.append(booking)
    return booking


def cancel_booking(bookings, booking_id):
    for booking in bookings:
        if booking["id"] == booking_id:
            booking["is_cancelled"] = True
            return True
    return False


def get_booking_status(is_cancelled):
    if is_cancelled:
        return "отменено"
    return "подтверждено"


def show_bookings(bookings):
    if not bookings:
        print("Бронирований пока нет.")
        return
    for booking in bookings:
        status = get_booking_status(booking["is_cancelled"])
        print(
            f"[{booking['id']}] {booking['user_name']}, "
            f"мероприятие #{booking['event_id']}, "
            f"билетов: {booking['tickets_count']}, статус: {status}"
        )
