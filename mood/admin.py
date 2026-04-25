from django.contrib import admin

# Register your models here.
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
        "created_at",
    )
    list_filter = ("mood_score", "date")
    search_fields = ("user__username", "user__email", "note")