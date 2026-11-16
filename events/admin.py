from django.contrib import admin

from bookings.models import Booking

from .models import Event


class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "venue", "seats", "price")
    list_display_links = ("name",)
    list_filter = ("name", "venue")
    list_per_page = 20
    ordering = ("date",)
    list_editable = ("seats",)

    inlines = (BookingInline,)
