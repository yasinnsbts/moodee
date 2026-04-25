from django.urls import path

from . import views

urlpatterns = [
    path("practices/", views.practices_view, name="practices"),
]
