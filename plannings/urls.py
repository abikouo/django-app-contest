from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.planning_list),
    path('<int:pk>/', views.planning_info),
    path('<int:pk>', views.planning_info),
]