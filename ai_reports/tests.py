from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from mood.models import MoodEntry
from .services import build_weekly_report


class WeeklyReportTests(TestCase):
    def test_report_mentions_low_sleep_and_factors(self):
        user = User.objects.create_user(
            username="report@example.com",
            email="report@example.com",
            password="test-password",
        )

        today = timezone.localdate()

        MoodEntry.objects.create(
            user=user,
            date=today,
            mood_score=2,
            wellbeing_score=2,
            activity_score=2,
            stress_score=5,
            anxiety_score=4,
            sleep_hours=5,
            factors="недосып, работа",
            note="Сложный рабочий день",
        )

        report = build_weekly_report(MoodEntry.objects.filter(user=user))
        insight_text = " ".join(report["insights"])

        self.assertIn("Сон", insight_text)
        self.assertIn("недосып", insight_text)
        self.assertTrue(report["recommendation"])


class AIReportViewTests(TestCase):
    def test_ai_report_returns_200_when_ai_analysis_disabled(self):
        user = User.objects.create_user(
            username="ai-disabled@example.com",
            email="ai-disabled@example.com",
            password="StrongPass12345!",
        )

        from accounts.models import UserSettings

        UserSettings.objects.create(
            user=user,
            ai_analysis_enabled=False,
        )

        self.client.force_login(user)

        response = self.client.get("/ai-report/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "AI-анализ отключён")
