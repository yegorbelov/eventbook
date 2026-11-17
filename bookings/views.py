from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, F, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from bookings.forms import BookingFilterForm, BookingForm
from bookings.models import Booking
from events.models import Event

PAGE_SIZE = 5


SORT_FIELDS = {
    "date": "event__date",
    "event": "event__name",
    "user": "user__name",
    "tickets": "tickets_count",
}
DEFAULT_SORT = "date"


def bookings(request):
    form = BookingFilterForm(request.GET)
    form.is_valid()
    data = form.cleaned_data

    bookings_data = Booking.objects.active()

    if data.get("q"):
        bookings_data = bookings_data.filter(
            Q(event__name__icontains=data["q"])
            | Q(user__name__icontains=data["q"])
        )
    if data.get("date"):
        bookings_data = bookings_data.for_date(data["date"])
    if data.get("event"):
        bookings_data = bookings_data.filter(event=data["event"])
    if data.get("user"):
        bookings_data = bookings_data.filter(user=data["user"])

    sort = data.get("sort") or DEFAULT_SORT
    sort_field = SORT_FIELDS[sort]
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
        "filter_form": form,
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


def booking_create(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            messages.success(request, f"Бронирование №{booking.pk} создано.")
            return redirect("bookings:detail", booking_id=booking.pk)
    else:
        initial = {}
        event_id = request.GET.get("event", "")
        if event_id.isdigit():
            initial["event"] = int(event_id)
        form = BookingForm(initial=initial)

    context = {
        "form": form,
        "title": "Новое бронирование",
        "submit_label": "Создать",
    }
    return render(request, "bookings/booking_form.html", context)


def booking_update(request, booking_id):
    booking = get_object_or_404(
        Booking.objects.select_related("event", "user"),
        pk=booking_id,
    )

    if booking.status != Booking.Status.ACTIVE:
        messages.error(
            request,
            "Изменять можно только активные бронирования.",
        )
        return redirect("bookings:detail", booking_id=booking.pk)

    if request.method == "POST":
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Изменения сохранены.")
            return redirect("bookings:detail", booking_id=booking.pk)
    else:
        form = BookingForm(instance=booking)

    context = {
        "form": form,
        "title": f"Бронирование №{booking.pk}",
        "submit_label": "Сохранить",
    }
    return render(request, "bookings/booking_form.html", context)


@require_POST
def booking_cancel(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)

    if booking.status == Booking.Status.ACTIVE:
        booking.cancel()
        messages.success(request, f"Бронирование №{booking.pk} отменено.")
    else:
        messages.error(request, "Это бронирование уже нельзя отменить.")
    return redirect("bookings:detail", booking_id=booking.pk)


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
