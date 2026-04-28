from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("entries/", views.entry_list_view, name="entry_list"),
    path("entries/new/", views.entry_create_view, name="entry_create"),
    path("entries/<int:pk>/edit/", views.entry_update_view, name="entry_update"),
    path("entries/<int:pk>/delete/", views.entry_delete_view, name="entry_delete"),
]
