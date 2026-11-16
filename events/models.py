from django.db import models
from django.db.models import Sum


class Event(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название",
    )
    date = models.DateTimeField(
        verbose_name="Дата и время",
    )
    venue = models.CharField(
        max_length=256,
        verbose_name="Место проведения",
    )
    seats = models.PositiveIntegerField(
        verbose_name="Количество мест",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
    )

    def booked_seats(self) -> int:
        total = self.bookings.filter(
            is_cancelled=False,
        ).aggregate(
            total=Sum("tickets_count")
        )["total"]
        return total or 0

    def has_capacity(self, tickets_count: int) -> bool:
        return self.seats - self.booked_seats() >= tickets_count

    def __str__(self) -> str:
        return f"{self.name} — {self.venue}, {self.date:%d.%m.%Y %H:%M}"

    class Meta:
        ordering = ["date", "pk"]
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
