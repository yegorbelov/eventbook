import os
import sqlite3
import sys
from contextlib import closing
from datetime import datetime
from decimal import Decimal
from pathlib import Path

import django
from django.conf import settings
from django.db import transaction
from django.utils import timezone

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

SOURCE_DB = BASE_DIR / "data" / "eventbook.sqlite"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eventbook.settings")
django.setup()

from bookings.models import Booking  # noqa: E402
from events.models import Event  # noqa: E402
from users.models import User  # noqa: E402

DATE_FORMATS = (
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M",
    "%d.%m.%Y %H:%M",
    "%Y-%m-%d",
    "%d.%m.%Y",
)


def parse_event_date(value) -> datetime:
    text = str(value).strip()
    for date_format in DATE_FORMATS:
        try:
            parsed = datetime.strptime(text, date_format)
            break
        except ValueError:
            continue
    else:
        raise ValueError(f"Неизвестный формат даты: {value!r}")

    if settings.USE_TZ and timezone.is_naive(parsed):
        parsed = timezone.make_aware(parsed)
    return parsed


def check_references(events, users, bookings) -> None:
    event_ids = {row["id"] for row in events}
    user_ids = {row["id"] for row in users}

    for row in bookings:
        if row["event_id"] not in event_ids:
            raise ValueError(
                f"Бронирование {row['id']}: нет события " f"{row['event_id']}"
            )
        if row["user_id"] not in user_ids:
            raise ValueError(
                f"Бронирование {row['id']}: нет пользователя "
                f"{row['user_id']}"
            )


def main() -> None:
    if not SOURCE_DB.exists():
        raise FileNotFoundError(f"Исходная база не найдена: {SOURCE_DB}")

    uri = f"{SOURCE_DB.as_uri()}?mode=ro"

    with closing(sqlite3.connect(uri, uri=True)) as connection:
        connection.row_factory = sqlite3.Row

        events = connection.execute(
            """
            SELECT id, name, date, venue, seats, price
            FROM events
            ORDER BY id
            """
        ).fetchall()
        users = connection.execute(
            """
            SELECT id, name
            FROM users
            ORDER BY id
            """
        ).fetchall()
        bookings = connection.execute(
            """
            SELECT id, event_id, user_id, tickets_count, is_cancelled
            FROM bookings
            ORDER BY id
            """
        ).fetchall()

    check_references(events, users, bookings)

    with transaction.atomic():
        for row in events:
            Event.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "name": row["name"],
                    "date": parse_event_date(row["date"]),
                    "venue": row["venue"],
                    "seats": row["seats"],
                    "price": Decimal(str(row["price"])),
                },
            )

        for row in users:
            User.objects.update_or_create(
                pk=row["id"],
                defaults={"name": row["name"]},
            )

        for row in bookings:
            Booking.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "event_id": row["event_id"],
                    "user_id": row["user_id"],
                    "tickets_count": row["tickets_count"],
                    "is_cancelled": bool(row["is_cancelled"]),
                },
            )

    print("Перенос данных завершён.")
    print(f"Мероприятий: {Event.objects.count()} (в источнике {len(events)})")
    print(f"Пользователей: {User.objects.count()} (в источнике {len(users)})")
    print(
        f"Бронирований: {Booking.objects.count()} "
        f"(в источнике {len(bookings)})"
    )


if __name__ == "__main__":
    main()
