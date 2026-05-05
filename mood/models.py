from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


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

    date = models.DateField(verbose_name="Дата записи")

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

    stress_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3,
        verbose_name="Стресс",
        help_text="1 — спокойно, 5 — очень напряжённо",
    )

    anxiety_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3,
        verbose_name="Тревожность",
        help_text="1 — низкая, 5 — высокая",
    )

    sleep_hours = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(24)],
        verbose_name="Сон, часов",
    )

    factors = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Факторы дня",
        help_text="Например: сон, работа, спорт, кофе, общение",
    )

    gratitude = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="За что благодарны",
    )

    note = models.TextField(
        blank=True,
        verbose_name="Заметка",
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
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date"],
                name="unique_mood_entry_per_user_date",
            ),
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
    def factor_list(self):
        return [
            factor.strip()
            for factor in self.factors.split(",")
            if factor.strip()
        ]
