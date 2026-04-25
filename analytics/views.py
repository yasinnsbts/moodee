from django.shortcuts import render

# Create your views here.
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
    elif period == "year":
        start_date = today - timedelta(days=364)
    else:
        period = "week"
        start_date = today - timedelta(days=6)

    entries = MoodEntry.objects.filter(
        user=request.user,
        date__gte=start_date,
        date__lte=today,
    ).order_by("date")

    average_score = entries.aggregate(avg=Avg("mood_score"))["avg"]

    labels = [entry.date.strftime("%d.%m") for entry in entries]
    values = [entry.mood_score for entry in entries]

    distribution_qs = entries.values("mood_score").annotate(count=Count("id"))
    distribution = {str(i): 0 for i in range(1, 6)}

    for item in distribution_qs:
        distribution[str(item["mood_score"])] = item["count"]

    context = {
        "period": period,
        "average_score": round(average_score, 1) if average_score else None,
        "chart_labels_json": json.dumps(labels, ensure_ascii=False),
        "chart_values_json": json.dumps(values),
        "distribution_json": json.dumps(distribution),
    }

    return render(request, "analytics/statistics.html", context)