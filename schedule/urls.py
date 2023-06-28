from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r"^$", views.home, name="index"),
    path("today/", views.create_schedule, name="today"),
    path("history/", views.history, name="history"),
    path("history/<int:id>/", views.history_detail, name="history_detail"),
    path("history/<int:id>", views.history_detail, name="history_detail"),
    path("history/delete/<int:id>/", views.history_delete, name="history_delete"),
    path("history/delete/<int:id>", views.history_delete, name="history_delete"),
]