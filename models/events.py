from typing import List, Optional

from models import Event


def add_event(
    events: List[Event], name: str, date: str, venue: str, seats: int, price: float
) -> Event:
    event_id = len(events) + 1
    event = Event(event_id, name, date, venue, seats, price)
    events.append(event)
    return event


def find_event(events: List[Event], event_id: int) -> Optional[Event]:
    for event in events:
        if event.id == event_id:
            return event
    return None


def sort_events_by_date(events: List[Event]) -> List[Event]:
    return sorted(events, key=lambda event: event.date)


def show_events(events: List[Event]) -> None:
    if not events:
        print("Мероприятий пока нет.")
        return
    for event in events:
        print(event)
