from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from mood.models import MoodEntry
from .services import build_weekly_report


@login_required
def ai_report_view(request):
    today = timezone.localdate()
    week_start = today - timedelta(days=6)

    entries = MoodEntry.objects.filter(
        user=request.user,
        date__gte=week_start,
        date__lte=today,
    ).order_by("date")

    report = build_weekly_report(entries)
    aggregates = report["averages"]

    average_mood = aggregates["avg_mood"]
    average_wellbeing = aggregates["avg_wellbeing"]
    average_activity = aggregates["avg_activity"]
    average_stress = aggregates["avg_stress"]
    average_anxiety = aggregates["avg_anxiety"]
    average_sleep = aggregates["avg_sleep"]

    context = {
        "insights": report["insights"],
        "recommendation": report["recommendation"],
        "average": round(average_mood, 1) if average_mood else None,
        "average_wellbeing": round(average_wellbeing, 1) if average_wellbeing else None,
        "average_activity": round(average_activity, 1) if average_activity else None,
        "average_stress": round(average_stress, 1) if average_stress else None,
        "average_anxiety": round(average_anxiety, 1) if average_anxiety else None,
        "average_sleep": round(average_sleep, 1) if average_sleep else None,
        "entries_count": entries.count(),
        "period_start": week_start,
        "period_end": today,
    }

    return render(request, "ai_reports/ai_report.html", context)
