from datetime import timedelta

from django.conf import settings
from django.core.validators import MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


class MoodEntry(models.Model):
    class MoodChoices(models.IntegerChoices):
        VERY_BAD = 1, "Очень плохо"
        BAD = 2, "Плохо"
        NEUTRAL = 3, "Нейтрально"
        GOOD = 4, "Хорошо"
        GREAT = 5, "Отлично"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mood_entries",
        verbose_name="Пользователь",
    )

    date = models.DateField(
        verbose_name="Дата записи",
    )

    mood_score = models.PositiveSmallIntegerField(
        choices=MoodChoices.choices,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Настроение",
    )

    wellbeing_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3,
        verbose_name="Самочувствие",
    )

    activity_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3,
        verbose_name="Активность",
    )

    note = models.TextField(
        blank=True,
        max_length=400,
        validators=[MaxLengthValidator(400)],
        verbose_name="Заметка",
        help_text="Не более 400 символов.",
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
        ordering = ["-date", "-created_at"]
        verbose_name = "Запись настроения"
        verbose_name_plural = "Записи настроения"
        indexes = [
            models.Index(fields=["user", "date"]),
        ]

    def __str__(self):
        return f"{self.user} — {self.date} — {self.mood_score}/5"

    @property
    def emoji(self):
        return {
            1: "😢",
            2: "😕",
            3: "😐",
            4: "🙂",
            5: "😍",
        }.get(self.mood_score, "😐")

    @property
    def edit_deadline(self):
        return self.created_at + timedelta(hours=24)

    @property
    def can_edit(self):
        if not self.created_at:
            return True

        return timezone.now() <= self.edit_deadline
