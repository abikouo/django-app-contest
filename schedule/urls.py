from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r"^$", views.home, name="index"),
    path("today/", views.create_schedule, name="today"),
]