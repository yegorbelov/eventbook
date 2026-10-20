import sqlite3

from django.shortcuts import render

DB_PATH = "data/eventbook.sqlite"


def bookings(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    bookings_list = conn.execute(
        """
        SELECT
            bookings.id,
            events.name AS event_name,
            events.date AS event_date,
            users.name AS user_name,
            bookings.tickets_count,
            bookings.is_cancelled
        FROM bookings
        JOIN events ON bookings.event_id = events.id
        JOIN users ON bookings.user_id = users.id
        WHERE bookings.is_cancelled = 0
        ORDER BY bookings.id
        """
    ).fetchall()
    conn.close()
    context = {"bookings": bookings_list}
    return render(request, "bookings/booking_list.html", context)


def booking_detail(request, booking_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    booking = conn.execute(
        """
        SELECT
            bookings.id,
            events.name AS event_name,
            events.id AS event_id,
            events.date AS event_date,
            users.name AS user_name,
            bookings.tickets_count,
            bookings.is_cancelled
        FROM bookings
        JOIN events ON bookings.event_id = events.id
        JOIN users ON bookings.user_id = users.id
        WHERE bookings.id = ?
        """,
        [booking_id],
    ).fetchone()
    conn.close()

    if booking is None:
        return render(
            request,
            "bookings/booking_detail.html",
            {"booking": None},
            status=404,
        )

    booking = dict(booking)
    context = {"booking": booking}
    return render(request, "bookings/booking_detail.html", context)


def statistics(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    statistics_data = conn.execute(
        """
        SELECT
            events.name AS event_name,
            COUNT(bookings.id) AS bookings_count
        FROM events
        LEFT JOIN bookings
            ON events.id = bookings.event_id
            AND bookings.is_cancelled = 0
        GROUP BY events.id, events.name
        ORDER BY bookings_count DESC
        """
    ).fetchall()
    conn.close()
    return render(
        request,
        "bookings/statistics.html",
        {"statistics": statistics_data},
    )
