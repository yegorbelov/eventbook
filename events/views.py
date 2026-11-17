from datetime import datetime

from django.contrib import messages
from django.db.models import ExpressionWrapper, F, IntegerField, Q, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, redirect, render

from bookings.models import Booking
from events.forms import EventForm
from events.models import Event


def with_free_seats(queryset):
    return queryset.annotate(
        booked=Coalesce(
            Sum(
                "bookings__tickets_count",
                filter=Q(bookings__status=Booking.Status.ACTIVE),
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

    if search:
        events_list = events_list.filter(name__icontains=search)

    events_list = events_list.order_by("date", "pk")

    context = {"events": events_list, "search": search}
    return render(request, "events/event_list.html", context)


def event_detail(request, slug):
    event = get_object_or_404(
        with_free_seats(Event.objects.all()),
        slug=slug,
    )

    event.available = event.free_seats > 0

    context = {"event": event, "available": event.available}
    return render(request, "events/event_detail.html", context)


def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            messages.success(request, f"Мероприятие «{event.name}» создано.")
            return redirect(event)
    else:
        form = EventForm()

    return render(request, "events/event_form.html", {"form": form})


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
