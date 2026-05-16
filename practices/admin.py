from django.contrib import admin

from .models import BreathingPractice


@admin.register(BreathingPractice)
class BreathingPracticeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "duration_minutes",
        "cycles",
        "is_active",
    )
    list_filter = (
        "is_active",
        "duration_minutes",
    )
    search_fields = (
        "title",
        "description",
        "instruction",
    )
