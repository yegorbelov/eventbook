from django.http import HttpResponse

from homepage.views import page
from models.bookings import find_booking_by_id
from storage import load_bookings, load_events, load_users


def _load_all():
    events_list = load_events("data/events.json")
    users_list = load_users("data/users.json")
    return load_bookings("data/bookings.json", events_list, users_list)


def bookings(request):
    items = ""
    for booking in _load_all():
        status = "отменено" if booking.is_cancelled else "активно"
        badge = "bg-secondary" if booking.is_cancelled else "bg-success"
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/bookings/{booking.id}/">
                {booking.event.name} – билетов: {booking.tickets_count}
            </a>
            <span class="badge {badge}">{status}</span>
        </li>
        """
    content = f"""
    <h1>Бронирования</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("EventBook – бронирования", content))


def booking_detail(request, booking_id):
    booking = find_booking_by_id(_load_all(), booking_id)
    if booking is None:
        content = """
        <h1 class="text-danger">Бронирование не найдено</h1>
        <a href="/bookings/" class="btn btn-outline-secondary">
            ← к списку бронирований
        </a>
        """
        return HttpResponse(
            page("Бронирование не найдено", content),
            status=404,
        )

    status = "отменено" if booking.is_cancelled else "активно"
    badge = "bg-secondary" if booking.is_cancelled else "bg-success"
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Бронирование №{booking.id}</h5>
            <p class="card-text">Мероприятие: {booking.event.name}</p>
            <p class="card-text">Билетов: {booking.tickets_count}</p>
            <p class="card-text">Пользователь: {booking.user.name}</p>
            <p class="card-text">
                Статус: <span class="badge {badge}">{status}</span>
            </p>
            <a href="/bookings/" class="btn btn-outline-secondary">
                ← к списку бронирований
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(f"Бронирование №{booking.id}", content))
