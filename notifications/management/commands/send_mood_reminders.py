from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.conf import settings

from accounts.models import UserSettings


class Command(BaseCommand):
    help = "Send mood diary reminders to users who enabled reminders"

    def handle(self, *args, **options):
        users = User.objects.filter(
            email__isnull=False,
            settings__reminder_enabled=True,
        ).exclude(email="")

        sent_count = 0

        for user in users:
            user_settings = UserSettings.objects.filter(user=user).first()

            reminder_time_text = ""
            if user_settings and user_settings.reminder_time:
                reminder_time_text = f" Вы выбрали время напоминания: {user_settings.reminder_time.strftime('%H:%M')}."

            subject = "Ладно: время отметить настроение"
            message = (
                f"Здравствуйте, {user.first_name or user.username}!\n\n"
                "Это мягкое напоминание заполнить дневник настроения в Ладно.\n"
                "Отметьте настроение, самочувствие, активность и короткую заметку о том, что повлияло на состояние.\n"
                f"{reminder_time_text}\n\n"
                "Это письмо отправлено из локальной версии проекта для демонстрации функциональности."
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            sent_count += 1

        self.stdout.write(self.style.SUCCESS(f"Reminders sent: {sent_count}"))
