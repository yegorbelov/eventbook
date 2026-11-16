from django.contrib import admin

from bookings.models import Booking
from events.models import Event


class EventBookingInline(admin.TabularInline):
    model = Booking
    extra = 0
    fields = ("user", "tickets_count", "status")
    autocomplete_fields = ("user",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "venue", "seats", "price", "is_large")
    list_display_links = ("name",)
    list_editable = ("seats",)
    search_fields = ("name", "venue")
    list_filter = ("date", "venue")
    ordering = ("date", "pk")
    list_per_page = 20
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("is_large",)
    inlines = (EventBookingInline,)
