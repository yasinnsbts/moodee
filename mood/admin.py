from django.contrib import admin

from .models import MoodEntry


@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "date",
        "mood_score",
        "wellbeing_score",
        "activity_score",
        "stress_score",
        "anxiety_score",
        "sleep_hours",
        "created_at",
    )
    list_filter = (
        "date",
        "mood_score",
        "wellbeing_score",
        "activity_score",
        "stress_score",
        "anxiety_score",
    )
    search_fields = (
        "user__username",
        "user__email",
        "note",
        "factors",
        "gratitude",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    date_hierarchy = "date"
    ordering = (
        "-date",
        "-created_at",
    )
