from django.shortcuts import render

from models.bookings import is_available
from models.events import find_event, sort_events_by_date
from storage import load_bookings, load_events, load_users


def events(request):
    events_list = sort_events_by_date(load_events("data/events.json"))
    context = {"events": events_list}
    return render(request, "events/event_list.html", context)


def event_detail(request, event_id):
    events_list = load_events("data/events.json")
    event = find_event(events_list, event_id)

    available = None
    if event is not None:
        users_list = load_users("data/users.json")
        bookings_list = load_bookings(
            "data/bookings.json", events_list, users_list
        )
        available = is_available(bookings_list, event, 1)

    context = {"event": event, "available": available}
    return render(
        request,
        "events/event_detail.html",
        context,
        status=404 if event is None else 200,
    )
