from django.core.validators import MinValueValidator
from django.db import models


class Booking(models.Model):
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
    is_cancelled = models.BooleanField(
        default=False,
        verbose_name="Бронирование отменено",
    )

    def __str__(self) -> str:
        status = "отменено" if self.is_cancelled else "подтверждено"
        return (
            f"[{self.pk}] {self.user.name} — {self.event.name}, "
            f"билетов: {self.tickets_count}, статус: {status}"
        )

    class Meta:
        ordering = ["pk"]
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
