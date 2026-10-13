from django.http import HttpResponse

from homepage.views import page
from models.bookings import is_available
from models.events import find_event, sort_events_by_date
from storage import load_bookings, load_events, load_users


def events(request):
    items = ""
    for event in sort_events_by_date(load_events("data/events.json")):
        text = f"{event.name} – {event.date}, {event.venue}"
        items += (
            '<li class="list-group-item">'
            f'<a href="/events/{event.id}/">{text}</a></li>'
        )
    content = f"""
    <h1>Мероприятия</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("EventBook – мероприятия", content))


def event_detail(request, event_id):
    events_list = load_events("data/events.json")
    event = find_event(events_list, event_id)
    if event is None:
        content = """
        <h1 class="text-danger">Мероприятие не найдено</h1>
        <a href="/events/" class="btn btn-outline-secondary">
            ← к списку мероприятий
        </a>
        """
        return HttpResponse(
            page("Мероприятие не найдено", content),
            status=404,
        )

    users_list = load_users("data/users.json")
    bookings_list = load_bookings(
        "data/bookings.json", events_list, users_list
    )
    available = is_available(bookings_list, event, 1)
    status = "есть места" if available else "мест нет"
    badge = "bg-success" if available else "bg-danger"

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{event.name}</h5>
            <p class="card-text"><strong>Дата:</strong> {event.date}</p>
            <p class="card-text">
                <strong>Место:</strong> {event.venue}
            </p>
            <p class="card-text">
                <strong>Цена билета:</strong> {event.price}
            </p>
            <p class="card-text">
                Наличие мест:
                <span class="badge {badge}">{status}</span>
            </p>
            <a href="/events/" class="btn btn-outline-secondary">
                ← к списку мероприятий
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(event.name, content), status=200)
