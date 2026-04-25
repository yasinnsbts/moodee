from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserSettings


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "theme",
        "reminder_enabled",
        "reminder_time",
        "ai_analysis_enabled",
    )