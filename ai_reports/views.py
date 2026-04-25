from django.shortcuts import render

# Create your views here.
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import render
from django.utils import timezone

from mood.models import MoodEntry


@login_required
def ai_report_view(request):
    today = timezone.localdate()
    week_start = today - timedelta(days=6)

    entries = MoodEntry.objects.filter(
        user=request.user,
        date__gte=week_start,
        date__lte=today,
    ).order_by("date")

    average = entries.aggregate(avg=Avg("mood_score"))["avg"]

    insights = []
    recommendation = ""

    if not entries.exists():
        insights.append("Пока недостаточно данных для анализа.")
        recommendation = "Добавляйте записи несколько дней подряд, чтобы увидеть первые закономерности."
    else:
        if average and average < 3:
            insights.append("Среднее настроение за неделю ниже нейтрального уровня.")
            recommendation = "Попробуйте снизить вечернюю нагрузку и добавить короткую дыхательную практику."
        elif average and average >= 4:
            insights.append("В целом настроение за неделю было устойчиво положительным.")
            recommendation = "Продолжайте отмечать факторы, которые помогают сохранять хорошее состояние."
        else:
            insights.append("Настроение за неделю было умеренным и менялось по дням.")
            recommendation = "Обратите внимание, какие события совпадают с улучшением или снижением настроения."

        low_days_count = entries.filter(mood_score__lte=2).count()

        if low_days_count >= 3:
            insights.append("Низкое настроение встречалось 3 или более раз за неделю.")

    context = {
        "insights": insights,
        "recommendation": recommendation,
        "average": round(average, 1) if average else None,
    }

    return render(request, "ai_reports/ai_report.html", context)