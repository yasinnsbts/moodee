from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from .models import UserSettings


class RegisterForm(forms.Form):
    first_name = forms.CharField(label="Имя", max_length=150)
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput,
    )
    consent = forms.BooleanField(
        label="Я согласен с условиями обработки персональных данных",
    )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")

        return email

    def clean_password1(self):
        password = self.cleaned_data["password1"]
        validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")

        return cleaned_data

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data["email"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password1"],
            first_name=self.cleaned_data["first_name"],
        )

        UserSettings.objects.create(user=user)

        return user


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = [
            "theme",
            "reminder_time",
            "ai_analysis_enabled",
        ]
        widgets = {
            "reminder_time": forms.TimeInput(attrs={"type": "time"}),
        }
