from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import RegisterForm, UserSettingsForm
from .models import UserSettings


class RegisterFormTests(TestCase):
    def test_register_form_creates_user_and_settings(self):
        form = RegisterForm(
            data={
                "first_name": "Ирина",
                "email": "new-user@example.com",
                "password1": "StrongPass12345!",
                "password2": "StrongPass12345!",
                "consent": "on",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)

        user = form.save()

        self.assertEqual(user.username, "new-user@example.com")
        self.assertEqual(user.email, "new-user@example.com")
        self.assertTrue(UserSettings.objects.filter(user=user).exists())

    def test_register_form_rejects_duplicate_email(self):
        User.objects.create_user(
            username="duplicate@example.com",
            email="duplicate@example.com",
            password="StrongPass12345!",
        )

        form = RegisterForm(
            data={
                "first_name": "Ирина",
                "email": "duplicate@example.com",
                "password1": "StrongPass12345!",
                "password2": "StrongPass12345!",
                "consent": "on",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)


class UserSettingsFormTests(TestCase):
    def test_user_settings_form_saves_reminder_and_ai_settings(self):
        user = User.objects.create_user(
            username="settings@example.com",
            email="settings@example.com",
            password="StrongPass12345!",
        )
        settings = UserSettings.objects.create(user=user)

        form = UserSettingsForm(
            data={
                "theme": UserSettings.ThemeChoices.LIGHT,
                "reminder_enabled": "on",
                "reminder_time": "20:30",
                "ai_analysis_enabled": "on",
            },
            instance=settings,
        )

        self.assertTrue(form.is_valid(), form.errors)

        updated_settings = form.save()

        self.assertTrue(updated_settings.reminder_enabled)
        self.assertTrue(updated_settings.ai_analysis_enabled)
        self.assertEqual(updated_settings.reminder_time.strftime("%H:%M"), "20:30")


class AccountViewsTests(TestCase):
    def test_profile_requires_login(self):
        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 302)

    def test_profile_page_for_logged_user_returns_200(self):
        user = User.objects.create_user(
            username="profile@example.com",
            email="profile@example.com",
            password="StrongPass12345!",
        )
        UserSettings.objects.create(user=user)

        self.client.force_login(user)

        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 200)

    def test_logout_uses_post(self):
        user = User.objects.create_user(
            username="logout@example.com",
            email="logout@example.com",
            password="StrongPass12345!",
        )

        self.client.force_login(user)

        response = self.client.post(reverse("logout"))

        self.assertIn(response.status_code, [200, 302])
