def add_event(events, name, date, venue, seats, price):
    event_id = len(events) + 1
    event = {
        "id": event_id,
        "name": name,
        "date": date,
        "venue": venue,
        "seats": seats,
        "price": price,
    }
    events.append(event)
    return event


def find_event(events, event_id):
    for event in events:
        if event["id"] == event_id:
            return event
    return None


def sort_events_by_date(events):
    return sorted(events, key=lambda event: event["date"])


def show_events(events):
    if not events:
        print("Мероприятий пока нет.")
        return
    for event in events:
        print(
            f"[{event['id']}] {event['name']} — {event['venue']}, "
            f"{event['date']}, мест: {event['seats']}, "
            f"цена: {event['price']} руб."
        )
