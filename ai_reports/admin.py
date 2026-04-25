from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import AIReport


@admin.register(AIReport)
class AIReportAdmin(admin.ModelAdmin):
    list_display = ("user", "period_start", "period_end", "created_at")
    search_fields = ("user__username", "user__email", "summary", "recommendation")