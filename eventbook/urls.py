from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("events/", include("events.urls")),
    path("bookings/", include("bookings.urls")),
]

handler404 = "homepage.views.page_not_found"
