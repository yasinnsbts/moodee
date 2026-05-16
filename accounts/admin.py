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
    list_filter = (
        "theme",
        "reminder_enabled",
        "ai_analysis_enabled",
    )
    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )
