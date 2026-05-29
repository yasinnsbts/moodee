from django.db import models

# Create your models here.
from django.conf import settings

class UserSettings(models.Model):
    class ThemeChoices(models.TextChoices):
        LIGHT = "light", "Светлая"
        DARK = "dark", "Тёмная"

    class GenderChoices(models.TextChoices):
        NOT_SPECIFIED = "not_specified", "Не указывать"
        MALE = "male", "Мужской"
        FEMALE = "female", "Женский"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="settings",
        verbose_name="Пользователь",
    )

    gender = models.CharField(
        max_length=20,
        choices=GenderChoices.choices,
        default=GenderChoices.NOT_SPECIFIED,
        verbose_name="Пол",
    )

    theme = models.CharField(
        max_length=20,
        choices=ThemeChoices.choices,
        default=ThemeChoices.LIGHT,
        verbose_name="Тема",
    )

    reminder_enabled = models.BooleanField(
        default=True,
        verbose_name="Напоминания включены",
    )

    reminder_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Время напоминания",
    )

    ai_analysis_enabled = models.BooleanField(
        default=True,
        verbose_name="AI-анализ включён",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создано",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Обновлено",
    )

    class Meta:
        verbose_name = "Настройки пользователя"
        verbose_name_plural = "Настройки пользователей"

    def __str__(self):
        return f"Настройки {self.user}"
