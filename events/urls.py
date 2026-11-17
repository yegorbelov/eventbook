from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("", views.events, name="list"),
    path("create/", views.event_create, name="event_create"),
    path("<slug:slug>/", views.event_detail, name="detail"),
    path("available/", views.available_events, name="available"),
]
