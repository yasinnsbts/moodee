from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TransactionTestCase
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
