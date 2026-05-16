from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from mood.models import MoodEntry

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
            "average_mood": None,
            "average_wellbeing": None,
            "average_activity": None,
            "average_stress": None,
            "average_anxiety": None,
            "average_sleep": None,
            "insights": [
                "AI-анализ отключён в настройках профиля.",
            ],
            "recommendation": (
                "Чтобы снова получать недельный анализ, включите AI-анализ в профиле."
            ),
            "frequent_positive_factors": [],
            "frequent_negative_factors": [],
            "frequent_keywords": [],
        }
        return render(request, "ai_reports/ai_report.html", context)

    today = timezone.localdate()
    period_start = today - timezone.timedelta(days=6)

    entries = (
        MoodEntry.objects
        .filter(
            user=request.user,
            date__gte=period_start,
            date__lte=today,
        )
        .order_by("date")
    )

    report = build_weekly_report(entries)

    context = {
        "ai_analysis_enabled": True,
        "period_start": period_start,
        "period_end": today,
        **report,
    }

    return render(request, "ai_reports/ai_report.html", context)
