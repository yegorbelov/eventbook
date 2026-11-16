from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Count, F, Q, Sum
from django.shortcuts import get_object_or_404, render

from bookings.models import Booking
from events.models import Event
from users.models import User

PAGE_SIZE = 5


SORT_FIELDS = {
    "date": "event__date",
    "event": "event__name",
    "user": "user__name",
    "tickets": "tickets_count",
}
DEFAULT_SORT = "date"


def bookings(request):
    search = request.GET.get("q", "").strip()
    event_date = request.GET.get("date", "").strip()
    event_id = request.GET.get("event", "").strip()
    user_id = request.GET.get("user", "").strip()
    sort = request.GET.get("sort", DEFAULT_SORT)
    error = None

    bookings_data = Booking.objects.active()

    if search:
        bookings_data = bookings_data.filter(
            Q(event__name__icontains=search) | Q(user__name__icontains=search)
        )

    if event_date:
        try:
            selected_date = datetime.strptime(event_date, "%Y-%m-%d").date()
        except ValueError:
            error = "Укажите корректную дату."
        else:
            bookings_data = bookings_data.for_date(selected_date)

    if event_id.isdigit():
        bookings_data = bookings_data.filter(event_id=int(event_id))
    if user_id.isdigit():
        bookings_data = bookings_data.filter(user_id=int(user_id))

    sort_field = SORT_FIELDS.get(sort, SORT_FIELDS[DEFAULT_SORT])
    bookings_data = (
        bookings_data.annotate(
            event_name=F("event__name"),
            event_date=F("event__date"),
            user_name=F("user__name"),
        )
        .values(
            "id",
            "event_name",
            "event_date",
            "user_name",
            "tickets_count",
            "status",
        )
        .order_by(sort_field, "id")
    )

    paginator = Paginator(bookings_data, PAGE_SIZE)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "bookings": page_obj,
        "page_obj": page_obj,
        "search": search,
        "booking_date": event_date,
        "selected_event": event_id,
        "selected_user": user_id,
        "sort": sort,
        "events": Event.objects.order_by("name"),
        "users": User.objects.order_by("name"),
        "error": error,
    }
    return render(request, "bookings/booking_list.html", context)


def booking_detail(request, booking_id):
    booking = get_object_or_404(
        Booking.objects.select_related("event", "user"),
        pk=booking_id,
    )
    return render(
        request,
        "bookings/booking_detail.html",
        {"booking": booking},
    )


def statistics(request):
    statistics_data = (
        Event.objects.annotate(
            event_name=F("name"),
            bookings_count=Count(
                "bookings",
                filter=Q(bookings__status=Booking.Status.ACTIVE),
            ),
        )
        .values("event_name", "bookings_count")
        .order_by("-bookings_count", "event_name")
    )

    totals = Booking.objects.aggregate(
        bookings=Count("id", filter=Q(status=Booking.Status.ACTIVE)),
        cancelled=Count("id", filter=Q(status=Booking.Status.CANCELLED)),
        completed=Count("id", filter=Q(status=Booking.Status.COMPLETED)),
        tickets=Sum(
            "tickets_count",
            filter=Q(status=Booking.Status.ACTIVE),
        ),
    )

    return render(
        request,
        "bookings/statistics.html",
        {"statistics": statistics_data, "totals": totals},
    )
