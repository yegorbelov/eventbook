from django import forms
from django.utils import timezone

from events.models import Event

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 МБ

DATETIME_FORMAT = "%Y-%m-%dT%H:%M"


class EventForm(forms.ModelForm):
    date = forms.DateTimeField(
        label="Дата и время",
        input_formats=[DATETIME_FORMAT],
        widget=forms.DateTimeInput(
            format=DATETIME_FORMAT,
            attrs={"type": "datetime-local", "class": "form-control"},
        ),
    )

    class Meta:
        model = Event
        fields = ["name", "date", "venue", "seats", "price", "image"]
        labels = {
            "name": "Название",
            "venue": "Место проведения",
            "seats": "Количество мест",
            "price": "Цена билета",
            "image": "Афиша",
        }
        help_texts = {
            "image": "Необязательно. JPEG или PNG, не больше 5 МБ.",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "venue": forms.TextInput(attrs={"class": "form-control"}),
            "seats": forms.NumberInput(
                attrs={"class": "form-control", "min": 1}
            ),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "min": 0, "step": "0.01"}
            ),
            "image": forms.ClearableFileInput(
                attrs={"class": "form-control", "accept": "image/*"}
            ),
        }

    def clean_date(self):
        date = self.cleaned_data["date"]
        if date < timezone.now():
            raise forms.ValidationError(
                "Нельзя создать мероприятие с датой в прошлом."
            )
        return date

    def clean_seats(self):
        seats = self.cleaned_data["seats"]
        if seats < 1:
            raise forms.ValidationError("Нужно указать хотя бы одно место.")
        return seats

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image and image.size > MAX_IMAGE_SIZE:
            raise forms.ValidationError("Файл больше 5 МБ.")
        return image
