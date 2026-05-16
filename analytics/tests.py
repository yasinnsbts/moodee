from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from mood.models import MoodEntry


class StatisticsViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="analytics@example.com",
            email="analytics@example.com",
            password="StrongPass12345!",
        )
        self.client.force_login(self.user)

    def test_statistics_requires_login(self):
        self.client.logout()

        response = self.client.get(reverse("statistics"))

        self.assertEqual(response.status_code, 302)

    def test_statistics_periods_return_200(self):
        today = timezone.localdate()

        MoodEntry.objects.create(
            user=self.user,
            date=today,
            mood_score=4,
            wellbeing_score=4,
            activity_score=3,
            stress_score=2,
            anxiety_score=2,
            sleep_hours=7,
            factors="сон, прогулка",
        )

        for period in ["week", "month", "year"]:
            response = self.client.get(reverse("statistics"), {"period": period})

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Аналитика настроения")
