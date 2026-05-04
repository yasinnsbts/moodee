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
            "note",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "mood_score": forms.RadioSelect,
            "wellbeing_score": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "activity_score": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "note": forms.Textarea(
                attrs={
                    "rows": 4,
                    "maxlength": 400,
                    "placeholder": "Что повлияло на настроение? До 400 символов.",
                }
            ),
        }
        help_texts = {
            "note": "Максимум 400 символов.",
        }

    def clean_note(self):
        note = self.cleaned_data.get("note", "")

        if len(note) > 400:
            raise forms.ValidationError("Заметка не должна превышать 400 символов.")

        return note
