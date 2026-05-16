from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase, TransactionTestCase
from django.utils import timezone

from .forms import MoodEntryForm
from .models import MoodEntry


class MoodEntryTests(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="test-password",
        )

    def test_factor_list_splits_comma_separated_values(self):
        entry = MoodEntry.objects.create(
            user=self.user,
            date=timezone.localdate(),
            mood_score=4,
            factors="сон, прогулка,  работа",
        )

        self.assertEqual(entry.factor_list, ["сон", "прогулка", "работа"])

    def test_only_one_entry_per_user_date(self):
        today = timezone.localdate()
        MoodEntry.objects.create(
            user=self.user,
            date=today,
            mood_score=4,
        )

        with self.assertRaises(IntegrityError):
            MoodEntry.objects.create(
                user=self.user,
                date=today,
                mood_score=3,
            )

    def test_form_rejects_duplicate_date_for_user(self):
        today = timezone.localdate()
        MoodEntry.objects.create(
            user=self.user,
            date=today,
            mood_score=4,
        )

        form = MoodEntryForm(
            data={
                "date": today,
                "mood_score": 3,
                "wellbeing_score": 3,
                "activity_score": 3,
                "stress_score": 3,
                "anxiety_score": 3,
                "sleep_hours": 7,
                "factors": "работа",
                "gratitude": "чай",
                "note": "",
            },
            user=self.user,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("date", form.errors)


class MoodEntryFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="form@example.com",
            email="form@example.com",
            password="test-password",
        )

    def test_form_rejects_note_longer_than_400_characters(self):
        form = MoodEntryForm(
            data={
                "date": timezone.localdate(),
                "mood_score": 3,
                "wellbeing_score": 3,
                "activity_score": 3,
                "stress_score": 3,
                "anxiety_score": 3,
                "sleep_hours": 7,
                "factors": "",
                "gratitude": "",
                "note": "а" * 401,
            },
            user=self.user,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("note", form.errors)


class MoodEntryEditWindowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="edit@example.com",
            email="edit@example.com",
            password="test-password",
        )
        self.client.force_login(self.user)

    def test_fresh_entry_can_be_opened_for_editing(self):
        entry = MoodEntry.objects.create(
            user=self.user,
            date=timezone.localdate(),
            mood_score=4,
        )

        response = self.client.get(f"/entries/{entry.pk}/edit/")

        self.assertEqual(response.status_code, 200)

    def test_entry_older_than_24_hours_cannot_be_edited(self):
        entry = MoodEntry.objects.create(
            user=self.user,
            date=timezone.localdate(),
            mood_score=4,
        )
        MoodEntry.objects.filter(pk=entry.pk).update(
            created_at=timezone.now() - timezone.timedelta(hours=25)
        )

        response = self.client.get(f"/entries/{entry.pk}/edit/")

        self.assertRedirects(response, "/entries/")


class SeedDemoDataCommandTests(TestCase):
    def test_seed_demo_data_command_creates_demo_content(self):
        from django.core.management import call_command

        from practices.models import BreathingPractice

        call_command("seed_demo_data")

        user = User.objects.get(username="irina@example.com")

        self.assertTrue(user.check_password("test12345"))
        self.assertTrue(MoodEntry.objects.filter(user=user).exists())
        self.assertTrue(BreathingPractice.objects.filter(is_active=True).exists())
