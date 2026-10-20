import json

from db.database import get_connection

EVENTS_FILE = "data/events.json"
USERS_FILE = "data/users.json"
BOOKINGS_FILE = "data/bookings.json"


def load_json(filename):
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def import_events(conn):
    events = load_json(EVENTS_FILE)

    conn.executemany(
        """
        INSERT INTO events (
            id, name, date, venue, seats, price
        )
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            name = excluded.name,
            date = excluded.date,
            venue = excluded.venue,
            seats = excluded.seats,
            price = excluded.price
        """,
        [
            (
                event["id"],
                event["name"],
                event["date"],
                event["venue"],
                event["seats"],
                event["price"],
            )
            for event in events
        ],
    )


def import_users(conn):
    users = load_json(USERS_FILE)

    conn.executemany(
        """
        INSERT INTO users (id, name)
        VALUES (?, ?)
        ON CONFLICT(id) DO UPDATE SET
            name = excluded.name
        """,
        [(user["id"], user["name"]) for user in users],
    )


def import_bookings(conn):
    bookings = load_json(BOOKINGS_FILE)

    conn.executemany(
        """
        INSERT INTO bookings (
            id, event_id, user_id,
            tickets_count, is_cancelled
        )
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            event_id = excluded.event_id,
            user_id = excluded.user_id,
            tickets_count = excluded.tickets_count,
            is_cancelled = excluded.is_cancelled
        """,
        [
            (
                booking["id"],
                booking["event_id"],
                booking["user_id"],
                booking["tickets_count"],
                int(booking["is_cancelled"]),
            )
            for booking in bookings
        ],
    )


def main():
    conn = get_connection()
    try:
        import_events(conn)
        import_users(conn)
        import_bookings(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
