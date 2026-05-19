from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import UserSettings
from mood.models import MoodEntry
from practices.models import BreathingPractice


class Command(BaseCommand):
    help = "Create demo user, mood entries, user settings and breathing practices."

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            username="irina@example.com",
            defaults={
                "email": "irina@example.com",
                "first_name": "Ирина",
            },
        )

        if created:
            user.set_password("test12345")
            user.save()
            self.stdout.write(self.style.SUCCESS("Demo user created."))
        else:
            if user.email != "irina@example.com":
                user.email = "irina@example.com"
                user.save(update_fields=["email"])

            self.stdout.write(self.style.WARNING("Demo user already exists."))

        settings, _ = UserSettings.objects.get_or_create(user=user)
        settings.reminder_enabled = True
        settings.reminder_time = "20:30"
        settings.ai_analysis_enabled = True
        settings.save()

        practices = [
            {
                "title": "Квадратное дыхание",
                "description": "Простая практика для снижения напряжения и возвращения внимания к телу.",
                "cycles": 4,
                "duration_minutes": 4,
                "instruction": "Вдохните на 4 счёта, задержите дыхание на 4, выдохните на 4 и снова задержите на 4.",
                "is_active": True,
            },
            {
                "title": "Дыхание 4–7–8",
                "description": "Мягкая практика для вечернего успокоения и подготовки ко сну.",
                "cycles": 4,
                "duration_minutes": 5,
                "instruction": "Вдохните на 4 счёта, задержите дыхание на 7, спокойно выдохните на 8.",
                "is_active": True,
            },
            {
                "title": "Спокойный выдох",
                "description": "Практика для моментов тревоги: выдох делается длиннее вдоха.",
                "cycles": 6,
                "duration_minutes": 3,
                "instruction": "Вдохните на 3 счёта и выдохните на 6. Повторите несколько циклов без напряжения.",
                "is_active": True,
            },
            {
                "title": "Пауза на тело",
                "description": "Короткое упражнение, чтобы заметить состояние тела и немного замедлиться.",
                "cycles": 5,
                "duration_minutes": 2,
                "instruction": "Сделайте спокойный вдох, на выдохе расслабьте плечи и челюсть. Повторите несколько раз.",
                "is_active": True,
            },
        ]

        for practice_data in practices:
            practice, practice_created = BreathingPractice.objects.update_or_create(
                title=practice_data["title"],
                defaults=practice_data,
            )

            if practice_created:
                self.stdout.write(
                    self.style.SUCCESS(f"Practice created: {practice.title}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Practice updated: {practice.title}")
                )

        today = timezone.localdate()

        entries = [
            {
                "days_ago": 13,
                "mood_score": 3,
                "wellbeing_score": 3,
                "activity_score": 2,
                "stress_score": 4,
                "anxiety_score": 3,
                "sleep_hours": 6.0,
                "factors": "работа, дедлайн",
                "gratitude": "Вечерняя прогулка",
                "note": "День был напряжённый, но удалось немного переключиться вечером.",
            },
            {
                "days_ago": 12,
                "mood_score": 4,
                "wellbeing_score": 4,
                "activity_score": 4,
                "stress_score": 2,
                "anxiety_score": 2,
                "sleep_hours": 7.5,
                "factors": "сон, прогулка",
                "gratitude": "Хороший сон",
                "note": "Больше энергии после нормального сна.",
            },
            {
                "days_ago": 11,
                "mood_score": 2,
                "wellbeing_score": 2,
                "activity_score": 2,
                "stress_score": 5,
                "anxiety_score": 4,
                "sleep_hours": 5.5,
                "factors": "работа, усталость",
                "gratitude": "Поддержка близких",
                "note": "Сложный день, много задач и мало отдыха.",
            },
            {
                "days_ago": 10,
                "mood_score": 3,
                "wellbeing_score": 3,
                "activity_score": 3,
                "stress_score": 3,
                "anxiety_score": 3,
                "sleep_hours": 6.5,
                "factors": "учёба, дорога",
                "gratitude": "Получилось закрыть часть задач",
                "note": "Обычный день без сильных провалов.",
            },
            {
                "days_ago": 9,
                "mood_score": 4,
                "wellbeing_score": 4,
                "activity_score": 5,
                "stress_score": 2,
                "anxiety_score": 2,
                "sleep_hours": 7.0,
                "factors": "спорт, прогулка",
                "gratitude": "Хорошая тренировка",
                "note": "Движение хорошо повлияло на настроение.",
            },
            {
                "days_ago": 8,
                "mood_score": 3,
                "wellbeing_score": 4,
                "activity_score": 3,
                "stress_score": 3,
                "anxiety_score": 2,
                "sleep_hours": 7.0,
                "factors": "дом, отдых",
                "gratitude": "Спокойный вечер",
                "note": "Удалось восстановиться после недели.",
            },
            {
                "days_ago": 7,
                "mood_score": 5,
                "wellbeing_score": 5,
                "activity_score": 4,
                "stress_score": 1,
                "anxiety_score": 1,
                "sleep_hours": 8.0,
                "factors": "отдых, семья",
                "gratitude": "День без спешки",
                "note": "Очень хороший день, спокойно и приятно.",
            },
            {
                "days_ago": 6,
                "mood_score": 4,
                "wellbeing_score": 4,
                "activity_score": 3,
                "stress_score": 2,
                "anxiety_score": 2,
                "sleep_hours": 7.5,
                "factors": "сон, работа",
                "gratitude": "Понятный план на день",
                "note": "Рабочий день прошёл ровно.",
            },
            {
                "days_ago": 5,
                "mood_score": 3,
                "wellbeing_score": 3,
                "activity_score": 3,
                "stress_score": 4,
                "anxiety_score": 3,
                "sleep_hours": 6.0,
                "factors": "дедлайн, учёба",
                "gratitude": "Помощь команды",
                "note": "Было напряжение из-за сроков.",
            },
            {
                "days_ago": 4,
                "mood_score": 4,
                "wellbeing_score": 4,
                "activity_score": 4,
                "stress_score": 2,
                "anxiety_score": 2,
                "sleep_hours": 7.0,
                "factors": "прогулка, спорт",
                "gratitude": "Свежий воздух",
                "note": "Прогулка помогла разгрузить голову.",
            },
            {
                "days_ago": 3,
                "mood_score": 2,
                "wellbeing_score": 3,
                "activity_score": 2,
                "stress_score": 5,
                "anxiety_score": 4,
                "sleep_hours": 5.0,
                "factors": "работа, мало сна",
                "gratitude": "Удалось лечь раньше",
                "note": "Сильно сказался недосып.",
            },
            {
                "days_ago": 2,
                "mood_score": 3,
                "wellbeing_score": 3,
                "activity_score": 3,
                "stress_score": 3,
                "anxiety_score": 3,
                "sleep_hours": 6.5,
                "factors": "дом, дела",
                "gratitude": "Тихий вечер",
                "note": "День был нейтральный.",
            },
            {
                "days_ago": 1,
                "mood_score": 4,
                "wellbeing_score": 4,
                "activity_score": 4,
                "stress_score": 2,
                "anxiety_score": 2,
                "sleep_hours": 7.5,
                "factors": "сон, прогулка, семья",
                "gratitude": "Хороший разговор",
                "note": "Настроение стало лучше после общения и прогулки.",
            },
            {
                "days_ago": 0,
                "mood_score": 4,
                "wellbeing_score": 4,
                "activity_score": 3,
                "stress_score": 2,
                "anxiety_score": 2,
                "sleep_hours": 7.0,
                "factors": "работа, порядок",
                "gratitude": "Удалось многое сделать",
                "note": "Спокойный продуктивный день.",
            },
        ]

        for raw_entry_data in entries:
            entry_data = raw_entry_data.copy()
            days_ago = entry_data.pop("days_ago")
            entry_date = today - timedelta(days=days_ago)

            entry, _ = MoodEntry.objects.update_or_create(
                user=user,
                date=entry_date,
                defaults=entry_data,
            )

            if days_ago > 0:
                demo_created_at = timezone.now() - timedelta(days=days_ago, hours=1)
                MoodEntry.objects.filter(pk=entry.pk).update(created_at=demo_created_at)

        self.stdout.write(
            self.style.SUCCESS(
                "Demo data is ready. Login: irina@example.com / test12345"
            )
        )
