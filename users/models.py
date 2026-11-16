from django.db import models


class User(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Имя пользователя",
    )

    def __str__(self) -> str:
        return f"[{self.pk}] {self.name}"

    class Meta:
        ordering = ["name", "pk"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
