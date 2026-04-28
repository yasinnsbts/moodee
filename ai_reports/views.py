from collections import Counter
from datetime import timedelta
import re

from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import render
from django.utils import timezone

from mood.models import MoodEntry


STOP_WORDS = {
    "и", "в", "во", "на", "но", "а", "я", "мы", "он", "она", "оно", "они",
    "что", "как", "это", "так", "с", "со", "по", "за", "от", "до", "для",
    "не", "нет", "было", "был", "была", "были", "очень", "немного", "день",
    "сегодня", "после", "перед", "при", "же", "то", "из", "у", "к",
}


def extract_keywords(notes):
    text = " ".join(notes).lower()
    words = re.findall(r"[а-яa-zё]{3,}", text)

    filtered_words = [
        word for word in words
        if word not in STOP_WORDS
    ]

    return Counter(filtered_words).most_common(5)


@login_required
def ai_report_view(request):
    today = timezone.localdate()
    week_start = today - timedelta(days=6)

    entries = MoodEntry.objects.filter(
        user=request.user,
        date__gte=week_start,
        date__lte=today,
    ).order_by("date")

    aggregates = entries.aggregate(
        avg_mood=Avg("mood_score"),
        avg_wellbeing=Avg("wellbeing_score"),
        avg_activity=Avg("activity_score"),
    )

    average_mood = aggregates["avg_mood"]
    average_wellbeing = aggregates["avg_wellbeing"]
    average_activity = aggregates["avg_activity"]

    insights = []
    recommendation = ""

    if not entries.exists():
        insights.append("Пока недостаточно данных для анализа.")
        recommendation = "Добавляйте записи несколько дней подряд, чтобы увидеть первые закономерности."
    else:
        if average_mood and average_mood < 3:
            insights.append("Среднее настроение за неделю ниже нейтрального уровня.")
        elif average_mood and average_mood >= 4:
            insights.append("Настроение за неделю в целом было устойчиво положительным.")
        else:
            insights.append("Настроение за неделю было умеренным и менялось по дням.")

        if average_wellbeing and average_wellbeing < 3:
            insights.append("Самочувствие часто было сниженным. Возможно, стоит обратить внимание на сон, отдых и нагрузку.")
        elif average_wellbeing and average_wellbeing >= 4:
            insights.append("Самочувствие в среднем было хорошим.")

        if average_activity and average_activity < 3:
            insights.append("Активность была ниже среднего. Мягкая прогулка или короткая разминка могут помочь поддержать состояние.")
        elif average_activity and average_activity >= 4:
            insights.append("Активность была высокой и могла поддерживать настроение.")

        low_days_count = entries.filter(mood_score__lte=2).count()

        if low_days_count >= 3:
            insights.append("Низкое настроение встречалось 3 или более раз за неделю.")

        notes = [entry.note for entry in entries if entry.note]
        keywords = extract_keywords(notes)

        if keywords:
            keywords_text = ", ".join([word for word, count in keywords])
            insights.append(f"В заметках часто встречались темы: {keywords_text}.")

        if average_mood and average_mood < 3:
            recommendation = "Попробуйте выбрать одну мягкую практику на вечер: дыхание 4–7–8, короткую прогулку или снижение вечерней нагрузки."
        elif average_activity and average_activity < 3:
            recommendation = "Попробуйте добавить небольшую регулярную активность: 10 минут прогулки или лёгкую разминку."
        elif average_wellbeing and average_wellbeing < 3:
            recommendation = "Обратите внимание на восстановление: сон, паузы в течение дня и спокойный вечерний ритуал."
        else:
            recommendation = "Продолжайте отмечать факторы, которые помогают сохранять стабильное состояние."

    context = {
        "insights": insights,
        "recommendation": recommendation,
        "average": round(average_mood, 1) if average_mood else None,
        "average_wellbeing": round(average_wellbeing, 1) if average_wellbeing else None,
        "average_activity": round(average_activity, 1) if average_activity else None,
        "entries_count": entries.count(),
        "period_start": week_start,
        "period_end": today,
    }

    return render(request, "ai_reports/ai_report.html", context)
