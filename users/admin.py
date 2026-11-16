from django.contrib import admin

from bookings.models import Booking
from users.models import User


class UserBookingInline(admin.TabularInline):
    model = Booking
    extra = 0
    fields = ("event", "tickets_count", "status")
    autocomplete_fields = ("event",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_display_links = ("name",)
    search_fields = ("name",)
    ordering = ("name", "pk")
    list_per_page = 20
    inlines = (UserBookingInline,)
