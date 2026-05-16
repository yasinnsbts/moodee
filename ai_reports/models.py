from django.conf import settings
from django.db import models


class AIReport(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ai_reports",
        verbose_name="Пользователь",
    )
    period_start = models.DateField(verbose_name="Начало периода")
    period_end = models.DateField(verbose_name="Конец периода")
    summary = models.TextField(verbose_name="Резюме")
    recommendation = models.TextField(
        blank=True,
        verbose_name="Рекомендация",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    class Meta:
        verbose_name = "AI-отчёт"
        verbose_name_plural = "AI-отчёты"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "period_start", "period_end"],
                name="unique_ai_report_per_user_period",
            ),
        ]

    def __str__(self):
        return f"AI-отчёт {self.user} за {self.period_start} — {self.period_end}"
