from django import forms

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
            "sleep_hours": forms.NumberInput(attrs={"min": 0, "max": 24, "step": 0.5}),
            "factors": forms.Textarea(
                attrs={
                    "rows": 3,
                    "maxlength": 400,
                    "placeholder": "Что повлияло на состояние? До 400 символов.",
                }
            ),
            "gratitude": forms.Textarea(
                attrs={
                    "rows": 3,
                    "maxlength": 400,
                    "placeholder": "Что хорошего произошло сегодня? До 400 символов.",
                }
            ),
            "note": forms.Textarea(
                attrs={
                    "rows": 4,
                    "maxlength": 400,
                    "placeholder": "Короткая заметка. До 400 символов.",
                }
            ),
        }
        help_texts = {
            "factors": "Максимум 400 символов.",
            "gratitude": "Максимум 400 символов.",
            "note": "Максимум 400 символов.",
        }

    def clean_factors(self):
        factors = self.cleaned_data.get("factors", "")

        if len(factors) > 400:
            raise forms.ValidationError("Поле факторов не должно превышать 400 символов.")

        return factors

    def clean_gratitude(self):
        gratitude = self.cleaned_data.get("gratitude", "")

        if len(gratitude) > 400:
            raise forms.ValidationError("Поле благодарности не должно превышать 400 символов.")

        return gratitude

    def clean_note(self):
        note = self.cleaned_data.get("note", "")

        if len(note) > 400:
            raise forms.ValidationError("Заметка не должна превышать 400 символов.")

        return note
