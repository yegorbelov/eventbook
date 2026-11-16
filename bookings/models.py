from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum


class BookingQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=Booking.Status.ACTIVE)

    def cancelled(self):
        return self.filter(status=Booking.Status.CANCELLED)

    def completed(self):
        return self.filter(status=Booking.Status.COMPLETED)

    def for_date(self, date):
        return self.filter(event__date__date=date)


class Booking(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Активно"
        CANCELLED = "cancelled", "Отменено"
        COMPLETED = "completed", "Завершено"

    event = models.ForeignKey(
        "events.Event",
        on_delete=models.PROTECT,
        related_name="bookings",
        verbose_name="Мероприятие",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="bookings",
        verbose_name="Пользователь",
    )
    tickets_count = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Количество билетов",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="Статус",
    )

    objects = BookingQuerySet.as_manager()

    def cancel(self) -> None:
        self.status = self.Status.CANCELLED
        self.save(update_fields=["status"])

    def clean(self) -> None:
        super().clean()
        if self.status != self.Status.ACTIVE or not self.event_id:
            return
        if not self.tickets_count:
            return
        booked = (
            Booking.objects.active()
            .filter(event_id=self.event_id)
            .exclude(pk=self.pk)
            .aggregate(total=Sum("tickets_count"))["total"]
            or 0
        )
        free = self.event.seats - booked
        if self.tickets_count > free:
            raise ValidationError(f"Недостаточно мест: свободно {free}.")

    def __str__(self) -> str:
        return (
            f"[{self.pk}] {self.user.name} — {self.event.name}, "
            f"билетов: {self.tickets_count}, "
            f"статус: {self.get_status_display().lower()}"
        )

    class Meta:
        ordering = ["pk"]
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
