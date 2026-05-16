from django import forms
from django.utils import timezone

from .models import MoodEntry


SCORE_CHOICES = [
    (1, "1 — очень плохо"),
    (2, "2 — плохо"),
    (3, "3 — нейтрально"),
    (4, "4 — хорошо"),
    (5, "5 — отлично"),
]


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

        labels = {
            "date": "Дата",
            "mood_score": "Настроение",
            "wellbeing_score": "Самочувствие",
            "activity_score": "Активность",
            "stress_score": "Стресс",
            "anxiety_score": "Тревожность",
            "sleep_hours": "Сон, часов",
            "factors": "Факторы",
            "gratitude": "Благодарность",
            "note": "Заметка",
        }

        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "mood_score": forms.Select(choices=SCORE_CHOICES),
            "wellbeing_score": forms.Select(choices=SCORE_CHOICES),
            "activity_score": forms.Select(choices=SCORE_CHOICES),
            "stress_score": forms.Select(choices=SCORE_CHOICES),
            "anxiety_score": forms.Select(choices=SCORE_CHOICES),
            "sleep_hours": forms.NumberInput(attrs={
                "min": "0",
                "max": "24",
                "step": "0.5",
                "placeholder": "Например, 7.5",
            }),
            "factors": forms.Textarea(attrs={
                "rows": 3,
                "maxlength": 400,
                "placeholder": "Что повлияло на состояние?",
            }),
            "gratitude": forms.Textarea(attrs={
                "rows": 3,
                "maxlength": 400,
                "placeholder": "За что сегодня благодарны?",
            }),
            "note": forms.Textarea(attrs={
                "rows": 4,
                "maxlength": 400,
                "placeholder": "Короткая заметка до 400 символов",
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        for field in self.fields.values():
            existing_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing_class} input-field".strip()

    def clean_date(self):
        date = self.cleaned_data["date"]

        if date > timezone.localdate():
            raise forms.ValidationError("Нельзя создать запись на будущую дату.")

        if self.user:
            existing_entries = MoodEntry.objects.filter(
                user=self.user,
                date=date,
            )

            if self.instance and self.instance.pk:
                existing_entries = existing_entries.exclude(pk=self.instance.pk)

            if existing_entries.exists():
                raise forms.ValidationError("Запись за эту дату уже существует.")

        return date

    def clean_sleep_hours(self):
        sleep_hours = self.cleaned_data.get("sleep_hours")

        if sleep_hours is None:
            return sleep_hours

        if sleep_hours < 0:
            raise forms.ValidationError("Количество часов сна не может быть меньше 0.")

        if sleep_hours > 24:
            raise forms.ValidationError("Количество часов сна не может быть больше 24.")

        return sleep_hours
