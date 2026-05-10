from collections import Counter
import re

from django.db.models import Avg


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


def build_factor_insights(entries):
    positive_factors = Counter()
    difficult_factors = Counter()

    for entry in entries:
        factors = entry.factor_list

        if entry.mood_score >= 4:
            positive_factors.update(factors)
        elif entry.mood_score <= 2:
            difficult_factors.update(factors)

    insights = []

    if positive_factors:
        factors = ", ".join([factor for factor, count in positive_factors.most_common(3)])
        insights.append(f"С хорошими днями чаще совпадали факторы: {factors}.")

    if difficult_factors:
        factors = ", ".join([factor for factor, count in difficult_factors.most_common(3)])
        insights.append(f"Со сложными днями чаще совпадали факторы: {factors}.")

    return insights


def build_weekly_report(entries):
    aggregates = entries.aggregate(
        avg_mood=Avg("mood_score"),
        avg_wellbeing=Avg("wellbeing_score"),
        avg_activity=Avg("activity_score"),
        avg_stress=Avg("stress_score"),
        avg_anxiety=Avg("anxiety_score"),
        avg_sleep=Avg("sleep_hours"),
    )

    average_mood = aggregates["avg_mood"]
    average_wellbeing = aggregates["avg_wellbeing"]
    average_activity = aggregates["avg_activity"]
    average_stress = aggregates["avg_stress"]
    average_anxiety = aggregates["avg_anxiety"]
    average_sleep = aggregates["avg_sleep"]

    insights = []
    recommendation = ""

    if not entries.exists():
        return {
            "insights": ["Пока недостаточно данных для анализа."],
            "recommendation": "Добавляйте записи несколько дней подряд, чтобы увидеть первые закономерности.",
            "averages": aggregates,
            "keywords": [],
        }

    if average_mood and average_mood < 3:
        insights.append("Среднее настроение за неделю ниже нейтрального уровня.")
    elif average_mood and average_mood >= 4:
        insights.append("Настроение за неделю в целом было устойчиво положительным.")
    else:
        insights.append("Настроение за неделю было умеренным и менялось по дням.")

    if average_wellbeing and average_wellbeing < 3:
        insights.append("Самочувствие часто было сниженным. Стоит мягко проверить сон, отдых и нагрузку.")
    elif average_wellbeing and average_wellbeing >= 4:
        insights.append("Самочувствие в среднем было хорошим.")

    if average_activity and average_activity < 3:
        insights.append("Активность была ниже среднего. Небольшая регулярная активность может поддержать состояние.")
    elif average_activity and average_activity >= 4:
        insights.append("Активность была высокой и могла поддерживать настроение.")

    if average_stress and average_stress >= 4:
        insights.append("Уровень стресса был высоким. Полезно отметить, какие события чаще всего совпадали с напряжением.")

    if average_anxiety and average_anxiety >= 4:
        insights.append("Тревожность часто была повышенной. Подойдут короткие grounding-практики и снижение вечерней нагрузки.")

    if average_sleep is not None and average_sleep < 6:
        insights.append("Сон в среднем был короче 6 часов. Это может заметно влиять на настроение и энергию.")

    low_days_count = entries.filter(mood_score__lte=2).count()

    if low_days_count >= 3:
        insights.append("Низкое настроение встречалось 3 или более раз за неделю.")

    insights.extend(build_factor_insights(entries))

    notes = [entry.note for entry in entries if entry.note]
    keywords = extract_keywords(notes)

    if keywords:
        keywords_text = ", ".join([word for word, count in keywords])
        insights.append(f"В заметках часто встречались темы: {keywords_text}.")

    if average_mood and average_mood < 3:
        recommendation = "Выберите одну мягкую практику на вечер: дыхание 4-7-8, короткую прогулку или спокойный план на завтра."
    elif average_stress and average_stress >= 4:
        recommendation = "Попробуйте 2-3 минуты квадратного дыхания и отметьте, какие задачи можно перенести или упростить."
    elif average_activity and average_activity < 3:
        recommendation = "Добавьте небольшую регулярную активность: 10 минут прогулки или лёгкую разминку."
    elif average_wellbeing and average_wellbeing < 3:
        recommendation = "Сфокусируйтесь на восстановлении: сон, паузы в течение дня и спокойный вечерний ритуал."
    else:
        recommendation = "Продолжайте отмечать факторы, которые помогают сохранять стабильное состояние."

    return {
        "insights": insights,
        "recommendation": recommendation,
        "averages": aggregates,
        "keywords": keywords,
    }
