from django.db import models
from django.db.models import BooleanField, Case, Sum, Value, When
from django.urls import reverse

from events.slugs import make_slug

LARGE_EVENT_SEATS = 100


class Event(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название",
    )
    slug = models.SlugField(
        max_length=280,
        null=True,
        blank=True,
        verbose_name="Slug (адрес страницы)",
        help_text="Латиница, цифры и дефис. Если пусто, создаётся сам.",
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
        help_text="Максимальное число билетов на мероприятие",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
    )

    is_large = models.GeneratedField(
        expression=Case(
            When(seats__gte=LARGE_EVENT_SEATS, then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        ),
        output_field=BooleanField(),
        db_persist=True,
        verbose_name="Большое мероприятие",
    )

    def booked_seats(self) -> int:
        total = self.bookings.active().aggregate(total=Sum("tickets_count"))[
            "total"
        ]
        return total or 0

    def has_capacity(self, tickets_count: int) -> bool:
        return self.seats - self.booked_seats() >= tickets_count

    def get_absolute_url(self) -> str:
        return reverse("events:detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            base = make_slug(self.name) or "event"
            slug, number = base, 2
            while Event.objects.filter(slug=slug).exists():
                slug = f"{base}-{number}"
                number += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name} — {self.venue}, {self.date:%d.%m.%Y %H:%M}"

    class Meta:
        ordering = ["date", "pk"]
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
