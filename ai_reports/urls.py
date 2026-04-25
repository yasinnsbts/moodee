from django.urls import path

from . import views

urlpatterns = [
    path("ai-report/", views.ai_report_view, name="ai_report"),
]
