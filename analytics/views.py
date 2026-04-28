from datetime import timedelta
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.shortcuts import render
from django.utils import timezone

from mood.models import MoodEntry


@login_required
def statistics_view(request):
    period = request.GET.get("period", "week")
    today = timezone.localdate()

    if period == "month":
        start_date = today - timedelta(days=29)
        period_title = "Месяц"
    elif period == "year":
        start_date = today - timedelta(days=364)
        period_title = "Год"
    else:
        period = "week"
        start_date = today - timedelta(days=6)
        period_title = "Неделя"

    entries = MoodEntry.objects.filter(
        user=request.user,
        date__gte=start_date,
        date__lte=today,
    ).order_by("date", "created_at")

    aggregates = entries.aggregate(
        avg_mood=Avg("mood_score"),
        avg_wellbeing=Avg("wellbeing_score"),
        avg_activity=Avg("activity_score"),
    )

    labels = [entry.date.strftime("%d.%m") for entry in entries]
    mood_values = [entry.mood_score for entry in entries]
    wellbeing_values = [entry.wellbeing_score for entry in entries]
    activity_values = [entry.activity_score for entry in entries]

    distribution_qs = entries.values("mood_score").annotate(count=Count("id"))
    distribution_map = {i: 0 for i in range(1, 6)}

    for item in distribution_qs:
        distribution_map[item["mood_score"]] = item["count"]

    mood_labels = {
        1: "Очень плохо",
        2: "Плохо",
        3: "Нейтрально",
        4: "Хорошо",
        5: "Отлично",
    }

    distribution_items = [
        {
            "score": score,
            "label": mood_labels[score],
            "count": count,
        }
        for score, count in distribution_map.items()
    ]

    best_entry = entries.order_by("-mood_score", "-date").first()
    worst_entry = entries.order_by("mood_score", "-date").first()

    context = {
        "period": period,
        "period_title": period_title,
        "entries_count": entries.count(),

        "average_score": round(aggregates["avg_mood"], 1) if aggregates["avg_mood"] else None,
        "average_wellbeing": round(aggregates["avg_wellbeing"], 1) if aggregates["avg_wellbeing"] else None,
        "average_activity": round(aggregates["avg_activity"], 1) if aggregates["avg_activity"] else None,

        "best_entry": best_entry,
        "worst_entry": worst_entry,

        "chart_labels_json": json.dumps(labels, ensure_ascii=False),
        "chart_mood_values_json": json.dumps(mood_values),
        "chart_wellbeing_values_json": json.dumps(wellbeing_values),
        "chart_activity_values_json": json.dumps(activity_values),

        "distribution_items": distribution_items,
    }

    return render(request, "analytics/statistics.html", context)
