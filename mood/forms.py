from django import forms
from django.core.exceptions import ValidationError

from .models import MoodEntry


class MoodEntryForm(forms.ModelForm):
    class Meta:
        model = MoodEntry
        fields = [
            "date",
            "mood_score",
            "wellbeing_score",
            "activity_score",
            "stress_score",
            "anxiety_score",
            "sleep_hours",
            "factors",
            "gratitude",
            "note",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "mood_score": forms.RadioSelect,
            "wellbeing_score": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "activity_score": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "stress_score": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "anxiety_score": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "sleep_hours": forms.NumberInput(
                attrs={
                    "min": 0,
                    "max": 24,
                    "step": "0.5",
                    "placeholder": "Например: 7.5",
                }
            ),
            "factors": forms.TextInput(
                attrs={
                    "placeholder": "сон, работа, прогулка, кофе",
                }
            ),
            "gratitude": forms.TextInput(
                attrs={
                    "placeholder": "Одна хорошая вещь за день",
                }
            ),
            "note": forms.Textarea(
                attrs={
                    "rows": 4,
                    "maxlength": 400,
                    "placeholder": "Что повлияло на настроение?",
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_date(self):
        date = self.cleaned_data["date"]

        if not self.user:
            return date

        duplicate_exists = MoodEntry.objects.filter(
            user=self.user,
            date=date,
        ).exclude(pk=self.instance.pk).exists()

        if duplicate_exists:
            raise ValidationError("На эту дату уже есть запись. Откройте её из истории и отредактируйте.")

        return date
