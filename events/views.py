import sqlite3

from django.shortcuts import render

DB_PATH = "data/eventbook.sqlite"


def events(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    events_list = conn.execute(
        """
        SELECT id, name, date, venue, seats, price
        FROM events
        ORDER BY date
        """
    ).fetchall()
    conn.close()
    context = {"events": events_list}
    return render(request, "events/event_list.html", context)


def event_detail(request, event_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    event = conn.execute(
        """
        SELECT id, name, date, venue, seats, price
        FROM events
        WHERE id = ?
        """,
        [event_id],
    ).fetchone()

    available = None
    free_seats = None
    if event is not None:
        booked = conn.execute(
            """
            SELECT COALESCE(SUM(tickets_count), 0)
            FROM bookings
            WHERE event_id = ? AND is_cancelled = 0
            """,
            [event_id],
        ).fetchone()[0]
        free_seats = event["seats"] - booked
        available = free_seats > 0

    conn.close()

    if event is None:
        return render(
            request,
            "events/event_detail.html",
            {"event": None, "available": False},
            status=404,
        )

    event = dict(event)
    event["available"] = available
    event["free_seats"] = free_seats

    context = {"event": event, "available": available}
    return render(request, "events/event_detail.html", context)


def available_events(request):
    booking_date = request.GET.get("date")
    events_list = []
    if booking_date:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        events_list = conn.execute(
            """
            SELECT
                e.id,
                e.name,
                e.date,
                e.venue,
                e.seats,
                e.price,
                e.seats - COALESCE(b.booked, 0) AS free_seats
            FROM events e
            LEFT JOIN (
                SELECT event_id, SUM(tickets_count) AS booked
                FROM bookings
                WHERE is_cancelled = 0
                GROUP BY event_id
            ) b ON e.id = b.event_id
            WHERE e.date = ?
              AND e.seats - COALESCE(b.booked, 0) > 0
            ORDER BY e.name
            """,
            [booking_date],
        ).fetchall()
        conn.close()
    context = {
        "events": events_list,
        "booking_date": booking_date,
    }
    return render(request, "events/available.html", context)
