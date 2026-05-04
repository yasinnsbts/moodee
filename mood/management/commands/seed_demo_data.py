from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import UserSettings
from mood.models import MoodEntry
from practices.models import BreathingPractice


class Command(BaseCommand):
    help = "Create demo data for Ладно"

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

        UserSettings.objects.get_or_create(user=user)

        today = timezone.localdate()

        demo_entries = [
            (0, 4, 4, 3, "Спокойный день, помогла прогулка у реки."),
            (1, 5, 5, 4, "Удачная встреча с командой и хороший сон."),
            (2, 3, 3, 3, "Много задач, но без сильного стресса."),
            (3, 2, 2, 2, "Устала после работы, было сложно сосредоточиться."),
            (4, 4, 4, 4, "Хороший день, помогла музыка и прогулка."),
            (5, 3, 3, 2, "Обычный день, немного не хватало энергии."),
            (6, 5, 4, 5, "Много активности и приятный вечер."),
        ]

        for days_ago, mood, wellbeing, activity, note in demo_entries:
            MoodEntry.objects.update_or_create(
                user=user,
                date=today - timedelta(days=days_ago),
                defaults={
                    "mood_score": mood,
                    "wellbeing_score": wellbeing,
                    "activity_score": activity,
                    "note": note,
                },
            )

        practices = [
            ("Квадратное дыхание", "Мягкая практика для стабилизации состояния.", 4, 2),
            ("Техника 4–7–8", "Практика для вечернего расслабления.", 3, 4),
            ("Успокаивающее дыхание", "Короткая техника для снижения напряжения.", 5, 3),
        ]

        for title, description, cycles, duration in practices:
            BreathingPractice.objects.update_or_create(
                title=title,
                defaults={
                    "description": description,
                    "cycles": cycles,
                    "duration_minutes": duration,
                    "is_active": True,
                },
            )

        self.stdout.write(self.style.SUCCESS("Demo data created."))
        self.stdout.write("Demo user: irina@example.com / test12345")
