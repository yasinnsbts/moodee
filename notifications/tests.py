from io import StringIO

from django.contrib.auth.models import User
from django.core import mail
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.utils import timezone

from accounts.models import UserSettings
from mood.models import MoodEntry


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="Ладно <noreply@ladno.local>",
)
class SendMoodRemindersCommandTests(TestCase):
    def test_command_sends_reminder_to_user_without_today_entry(self):
        user = User.objects.create_user(
            username="reminder@example.com",
            email="reminder@example.com",
            password="StrongPass12345!",
        )
        UserSettings.objects.create(
            user=user,
            reminder_enabled=True,
        )

        output = StringIO()
        call_command("send_mood_reminders", stdout=output)

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Ладно", mail.outbox[0].subject)

    def test_command_skips_user_with_today_entry(self):
        user = User.objects.create_user(
            username="skip@example.com",
            email="skip@example.com",
            password="StrongPass12345!",
        )
        UserSettings.objects.create(
            user=user,
            reminder_enabled=True,
        )

        MoodEntry.objects.create(
            user=user,
            date=timezone.localdate(),
            mood_score=4,
        )

        output = StringIO()
        call_command("send_mood_reminders", stdout=output)

        self.assertEqual(len(mail.outbox), 0)
        self.assertIn("Skipped", output.getvalue())

    def test_command_does_not_send_when_reminders_disabled(self):
        user = User.objects.create_user(
            username="disabled@example.com",
            email="disabled@example.com",
            password="StrongPass12345!",
        )
        UserSettings.objects.create(
            user=user,
            reminder_enabled=False,
        )

        output = StringIO()
        call_command("send_mood_reminders", stdout=output)

        self.assertEqual(len(mail.outbox), 0)
