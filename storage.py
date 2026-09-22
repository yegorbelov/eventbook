import json
from typing import List

from models import Booking, Event, User


def load_json(filename: str) -> list:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, данные не загружены.")
        return []


def save_json(filename: str, data: list) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_events(filename: str) -> List[Event]:
    raw_events = load_json(filename)
    return [
        Event(item["id"], item["name"], item["date"], item["venue"], item["seats"], item["price"])
        for item in raw_events
    ]


def save_events(filename: str, events: List[Event]) -> None:
    data = [
        {
            "id": e.id,
            "name": e.name,
            "date": e.date,
            "venue": e.venue,
            "seats": e.seats,
            "price": e.price,
        }
        for e in events
    ]
    save_json(filename, data)


def load_users(filename: str) -> List[User]:
    raw_users = load_json(filename)
    return [User(item["id"], item["name"]) for item in raw_users]


def save_users(filename: str, users: List[User]) -> None:
    data = [{"id": u.id, "name": u.name} for u in users]
    save_json(filename, data)


def load_bookings(filename: str, events: List[Event], users: List[User]) -> List[Booking]:
    raw_bookings = load_json(filename)
    bookings = []
    for item in raw_bookings:
        event = next((e for e in events if e.id == item["event_id"]), None)
        user = next((u for u in users if u.id == item["user_id"]), None)
        if event is None or user is None:
            continue
        booking = Booking(item["id"], event, user, item["tickets_count"])
        booking.is_cancelled = item["is_cancelled"]
        bookings.append(booking)
    return bookings


def save_bookings(filename: str, bookings: List[Booking]) -> None:
    data = [
        {
            "id": b.id,
            "event_id": b.event.id,
            "user_id": b.user.id,
            "tickets_count": b.tickets_count,
            "is_cancelled": b.is_cancelled,
        }
        for b in bookings
    ]
    save_json(filename, data)
