from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from mood.models import MoodEntry


class Command(BaseCommand):
    help = "Send mood diary reminders to users who enabled reminders."

    def handle(self, *args, **options):
        today = timezone.localdate()

        users = (
            User.objects
            .filter(
                email__isnull=False,
                settings__reminder_enabled=True,
            )
            .exclude(email="")
            .select_related("settings")
        )

        sent_count = 0
        skipped_count = 0

        for user in users:
            has_today_entry = MoodEntry.objects.filter(
                user=user,
                date=today,
            ).exists()

            if has_today_entry:
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipped {user.email}: entry for today already exists."
                    )
                )
                continue

            user_settings = getattr(user, "settings", None)

            reminder_time = (
                user_settings.reminder_time.strftime("%H:%M")
                if user_settings and user_settings.reminder_time
                else "вечером"
            )

            subject = "Ладно: время отметить настроение"
            message = (
                f"Здравствуйте, {user.first_name or user.username}!\n\n"
                f"Вы включили напоминания в приложении «Ладно».\n"
                f"Запланированное время напоминания: {reminder_time}.\n\n"
                f"Зайдите в дневник и отметьте своё состояние за сегодня."
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                recipient_list=[user.email],
                fail_silently=False,
            )

            sent_count += 1
            self.stdout.write(
                self.style.SUCCESS(f"Reminder sent to {user.email}")
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Sent: {sent_count}. Skipped: {skipped_count}."
            )
        )
