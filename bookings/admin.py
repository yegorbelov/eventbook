from django.contrib import admin

from bookings.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "event", "user", "tickets_count", "status")
    list_display_links = ("id",)
    list_editable = ("status",)
    list_select_related = ("event", "user")
    search_fields = ("event__name", "user__name")
    list_filter = ("status", "event")
    ordering = ("-pk",)
    list_per_page = 20
    autocomplete_fields = ("event", "user")
    actions = ("cancel_selected", "complete_selected")

    @admin.action(description="Отменить выбранные бронирования")
    def cancel_selected(self, request, queryset):
        updated = queryset.update(status=Booking.Status.CANCELLED)
        self.message_user(request, f"Отменено бронирований: {updated}")

    @admin.action(description="Отметить выбранные как завершённые")
    def complete_selected(self, request, queryset):
        updated = queryset.update(status=Booking.Status.COMPLETED)
        self.message_user(request, f"Завершено бронирований: {updated}")
