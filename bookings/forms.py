from django import forms
from django.utils import timezone

from bookings.models import Booking
from events.models import Event
from users.models import User

SORT_CHOICES = [
    ("date", "По дате мероприятия"),
    ("event", "По мероприятию"),
    ("user", "По пользователю"),
    ("tickets", "По числу билетов"),
]


class BookingFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        max_length=100,
        label="Поиск",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Мероприятие или пользователь",
            }
        ),
    )

    date = forms.DateField(
        required=False,
        label="Дата мероприятия",
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={"type": "date", "class": "form-control"},
        ),
    )
    event = forms.ModelChoiceField(
        queryset=Event.objects.order_by("name"),
        required=False,
        label="Мероприятие",
        empty_label="Все мероприятия",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    user = forms.ModelChoiceField(
        queryset=User.objects.order_by("name"),
        required=False,
        label="Пользователь",
        empty_label="Все пользователи",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    sort = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        label="Сортировка",
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["event", "user", "tickets_count"]
        labels = {
            "event": "Мероприятие",
            "user": "Пользователь",
            "tickets_count": "Количество билетов",
        }
        help_texts = {
            "event": "Выберите мероприятие, которое ещё не прошло.",
            "tickets_count": "Не больше, чем осталось свободных мест.",
        }
        widgets = {
            "event": forms.Select(attrs={"class": "form-select"}),
            "user": forms.Select(attrs={"class": "form-select"}),
            "tickets_count": forms.NumberInput(
                attrs={"class": "form-control", "min": 1}
            ),
        }

    def clean_event(self):
        event = self.cleaned_data["event"]
        if event.date < timezone.now():
            raise forms.ValidationError(
                "Нельзя забронировать билеты на прошедшее мероприятие."
            )
        return event
