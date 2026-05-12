from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models

class UserSettings(models.Model):
    class ThemeChoices(models.TextChoices):
        LIGHT = "light", "Светлая"
        DARK = "dark", "Тёмная"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="settings",
        verbose_name="Пользователь",
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