from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import BreathingPractice


class PracticesViewTests(TestCase):
    def test_practices_requires_login(self):
        response = self.client.get(reverse("practices"))

        self.assertEqual(response.status_code, 302)

    def test_practices_page_shows_only_active_practices(self):
        user = User.objects.create_user(
            username="practice@example.com",
            email="practice@example.com",
            password="StrongPass12345!",
        )
        self.client.force_login(user)

        BreathingPractice.objects.create(
            title="Активная практика",
            description="Описание",
            cycles=4,
            duration_minutes=3,
            instruction="Дышите спокойно.",
            is_active=True,
        )

        BreathingPractice.objects.create(
            title="Неактивная практика",
            description="Не должна отображаться",
            cycles=4,
            duration_minutes=3,
            instruction="",
            is_active=False,
        )

        response = self.client.get(reverse("practices"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Активная практика")
        self.assertNotContains(response, "Неактивная практика")
