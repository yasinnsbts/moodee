from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import BreathingPractice


@admin.register(BreathingPractice)
class BreathingPracticeAdmin(admin.ModelAdmin):
    list_display = ("title", "cycles", "duration_minutes", "is_active")
    list_filter = ("is_active",)