from datetime import datetime

from django.db.models import ExpressionWrapper, F, IntegerField, Q, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, render

from events.models import Event


def with_free_seats(queryset):
    """Добавляет к мероприятиям занятые и свободные места.

    Учитываются только активные бронирования: отменённые места
    не занимают. Мероприятия без бронирований остаются в выборке,
    у них booked = 0.
    """
    return queryset.annotate(
        booked=Coalesce(
            Sum(
                "bookings__tickets_count",
                filter=Q(bookings__is_cancelled=False),
            ),
            0,
            output_field=IntegerField(),
        ),
    ).annotate(
        free_seats=ExpressionWrapper(
            F("seats") - F("booked"),
            output_field=IntegerField(),
        ),
    )


def events(request):
    search = request.GET.get("q", "").strip()

    events_list = Event.objects.all()

    # Поиск по названию мероприятия.
    if search:
        events_list = events_list.filter(name__icontains=search)

    events_list = events_list.order_by("date", "pk")

    context = {"events": events_list, "search": search}
    return render(request, "events/event_list.html", context)


def event_detail(request, event_id):
    # 404 формируется внутри get_object_or_404, если записи нет.
    event = get_object_or_404(
        with_free_seats(Event.objects.all()),
        pk=event_id,
    )

    # Атрибуты, которые раньше добавлялись в словарь.
    event.available = event.free_seats > 0

    context = {"event": event, "available": event.available}
    return render(request, "events/event_detail.html", context)


def available_events(request):
    booking_date = request.GET.get("date", "").strip()
    events_list = []
    error = None

    if booking_date:
        try:
            selected_date = datetime.strptime(booking_date, "%Y-%m-%d").date()
        except ValueError:
            error = "Укажите корректную дату."
        else:
            # Мероприятия на выбранную дату, из которых исключены
            # те, где не осталось свободных мест.
            events_list = (
                with_free_seats(Event.objects.filter(date__date=selected_date))
                .exclude(free_seats__lte=0)
                .order_by("name")
            )

    context = {
        "events": events_list,
        "booking_date": booking_date,
        "error": error,
    }
    return render(request, "events/available.html", context)
