from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from mood.models import MoodEntry

from .models import AIReport
from .services import build_weekly_report


@login_required
def ai_report_view(request):
    user_settings = getattr(request.user, "settings", None)

    if user_settings and not user_settings.ai_analysis_enabled:
        context = {
            "ai_analysis_enabled": False,
            "period_start": None,
            "period_end": None,
            "entries_count": 0,
            "insights": [
                "AI-анализ отключён в настройках профиля.",
            ],
            "recommendation": (
                "Чтобы снова получать недельный анализ, включите AI-анализ в профиле."
            ),
            "average": None,
            "average_wellbeing": None,
            "average_activity": None,
            "average_stress": None,
            "average_anxiety": None,
            "average_sleep": None,
            "saved_report": None,
        }

        return render(request, "ai_reports/ai_report.html", context)

    today = timezone.localdate()
    week_start = today - timedelta(days=6)

    entries = (
        MoodEntry.objects
        .filter(
            user=request.user,
            date__gte=week_start,
            date__lte=today,
        )
        .order_by("date")
    )

    report = build_weekly_report(entries)
    aggregates = report["averages"]

    average_mood = aggregates["avg_mood"]
    average_wellbeing = aggregates["avg_wellbeing"]
    average_activity = aggregates["avg_activity"]
    average_stress = aggregates["avg_stress"]
    average_anxiety = aggregates["avg_anxiety"]
    average_sleep = aggregates["avg_sleep"]

    insights = report["insights"]
    recommendation = report["recommendation"]

    summary = "\n".join(insights)

    saved_report, _ = AIReport.objects.update_or_create(
        user=request.user,
        period_start=week_start,
        period_end=today,
        defaults={
            "summary": summary,
            "recommendation": recommendation,
        },
    )

    context = {
        "ai_analysis_enabled": True,
        "insights": insights,
        "recommendation": recommendation,
        "average": round(average_mood, 1) if average_mood else None,
        "average_wellbeing": round(average_wellbeing, 1) if average_wellbeing else None,
        "average_activity": round(average_activity, 1) if average_activity else None,
        "average_stress": round(average_stress, 1) if average_stress else None,
        "average_anxiety": round(average_anxiety, 1) if average_anxiety else None,
        "average_sleep": round(average_sleep, 1) if average_sleep else None,
        "entries_count": entries.count(),
        "period_start": week_start,
        "period_end": today,
        "saved_report": saved_report,
    }

    return render(request, "ai_reports/ai_report.html", context)
